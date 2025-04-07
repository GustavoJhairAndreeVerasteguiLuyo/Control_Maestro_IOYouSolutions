       IDENTIFICATION DIVISION.
       PROGRAM-ID. IOT-AUTH-DEVICE.

       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01 BIOMETRICO-ENTRADA     PIC X(20) VALUE "USUARIO123".
       01 BIOMETRICO-REGISTRADO  PIC X(20) VALUE "USUARIO123".
       01 MENSAJE                PIC X(50).

       PROCEDURE DIVISION.
       INICIO.
           DISPLAY "⏳ Verificando biometría..."
           IF BIOMETRICO-ENTRADA = BIOMETRICO-REGISTRADO
               MOVE "✅ Acceso autorizado: usuario válido" TO MENSAJE
           ELSE
               MOVE "❌ Acceso denegado: usuario no reconocido" TO MENSAJE
           END-IF
           DISPLAY MENSAJE
           STOP RUN.
