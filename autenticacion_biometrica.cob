       IDENTIFICATION DIVISION.
       PROGRAM-ID. IOT-AUTH-DEVICE.

       ENVIRONMENT DIVISION.
       CONFIGURATION SECTION.

       DATA DIVISION.
       WORKING-STORAGE SECTION.

       01 USUARIOS-REGISTRADOS.
          05 USUARIO-1   PIC X(20) VALUE "USUARIO123".
          05 USUARIO-2   PIC X(20) VALUE "DISPOSITIVO456".
          05 USUARIO-3   PIC X(20) VALUE "SENSOR789".

       01 ENTRADA-BIOMETRICA.
          05 BIOMETRICO-RAW      PIC X(20) VALUE "usuario123".
          05 BIOMETRICO-LIMPIO   PIC X(20).

       01 MENSAJE                PIC X(60).
       01 VALIDACION-EXITOSA     PIC X VALUE 'N'.
       01 I                      PIC 9 VALUE 1.
       01 LIMITE-USUARIOS        PIC 9 VALUE 3.

       PROCEDURE DIVISION.
       INICIO.
           DISPLAY "⏳ Verificando biometría de dispositivo IoT..."
           
           PERFORM NORMALIZAR-BIOMETRICO

           PERFORM VALIDAR-USUARIO
           
           IF VALIDACION-EXITOSA = 'S'
               MOVE "✅ Acceso autorizado: dispositivo reconocido." TO MENSAJE
           ELSE
               MOVE "❌ Acceso denegado: no se reconoce el dispositivo." TO MENSAJE
           END-IF

           DISPLAY MENSAJE
           STOP RUN.

       NORMALIZAR-BIOMETRICO.
           PERFORM VARYING I FROM 1 BY 1 UNTIL I > 20
               MOVE FUNCTION UPPER-CASE(BIOMETRICO-RAW(I:1))
                    TO BIOMETRICO-LIMPIO(I:1)
           END-PERFORM.

       VALIDAR-USUARIO.
           PERFORM VARYING I FROM 1 BY 1 UNTIL I > LIMITE-USUARIOS OR VALIDACION-EXITOSA = 'S'
               EVALUATE I
                   WHEN 1
                       IF BIOMETRICO-LIMPIO = FUNCTION UPPER-CASE(USUARIO-1)
                           MOVE 'S' TO VALIDACION-EXITOSA
                   WHEN 2
                       IF BIOMETRICO-LIMPIO = FUNCTION UPPER-CASE(USUARIO-2)
                           MOVE 'S' TO VALIDACION-EXITOSA
                   WHEN 3
                       IF BIOMETRICO-LIMPIO = FUNCTION UPPER-CASE(USUARIO-3)
                           MOVE 'S' TO VALIDACION-EXITOSA
               END-EVALUATE
           END-PERFORM.

