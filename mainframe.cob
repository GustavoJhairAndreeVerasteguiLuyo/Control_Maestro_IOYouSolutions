       IDENTIFICATION DIVISION.
       PROGRAM-ID. SECURITY-BOOT.

       ENVIRONMENT DIVISION.
       INPUT-OUTPUT SECTION.
       FILE-CONTROL.

       DATA DIVISION.
       WORKING-STORAGE SECTION.

       * Mensajes
       01 WS-MESSAGE             PIC X(30) VALUE ">> Booting...".
       01 WS-LOAD-MESSAGE        PIC X(30) VALUE ">> System Loaded Successfully.".
       01 WS-ERROR-MESSAGE       PIC X(30) VALUE ">> Critical Boot Error.".
       01 WS-JUMP-MESSAGE        PIC X(30) VALUE ">> Jumping to firmware...".

       * Estado general
       01 FUNCTION-OK            PIC X VALUE SPACE.
       01 FIRMWARE-READ          PIC X VALUE SPACE.
       01 HW-INIT                PIC X VALUE SPACE.
       01 FS-MOUNTED             PIC X VALUE SPACE.

       PROCEDURE DIVISION.
       MAIN-PROCEDURE.
           DISPLAY WS-MESSAGE
           PERFORM INITIALIZE-VIDEO
           PERFORM READ-FIRMWARE
           PERFORM INIT-HARDWARE
           PERFORM INIT-FILESYSTEM

           IF FUNCTION-OK = 'Y'
               DISPLAY WS-LOAD-MESSAGE
               PERFORM START-FIRMWARE
           ELSE
               DISPLAY WS-ERROR-MESSAGE
           END-IF

           STOP RUN.

       INITIALIZE-VIDEO.
           DISPLAY " - Setting video mode...".
           DISPLAY " - Paging and segmentation setup complete.".

       READ-FIRMWARE.
           DISPLAY " - Reading firmware sector...".
           IF FIRMWARE-READ NOT = 'F'
               MOVE 'Y' TO FIRMWARE-READ
               DISPLAY "   -> Firmware loaded OK."
           ELSE
               MOVE 'N' TO FUNCTION-OK
               DISPLAY "   -> Firmware read failed."
           END-IF.

       INIT-HARDWARE.
           DISPLAY " - Initializing USB and Serial COM...".
           IF HW-INIT NOT = 'F'
               MOVE 'Y' TO HW-INIT
               DISPLAY "   -> USB and Serial initialized."
           ELSE
               MOVE 'N' TO FUNCTION-OK
               DISPLAY "   -> Hardware init failed."
           END-IF.

       INIT-FILESYSTEM.
           DISPLAY " - Mounting filesystem...".
           IF FS-MOUNTED NOT = 'F'
               MOVE 'Y' TO FS-MOUNTED
               DISPLAY "   -> Filesystem mounted."
               PERFORM VERIFY-STATUS
           ELSE
               MOVE 'N' TO FUNCTION-OK
               DISPLAY "   -> Filesystem mount failed."
           END-IF.

       VERIFY-STATUS.
           IF FIRMWARE-READ = 'Y' AND
              HW-INIT = 'Y' AND
              FS-MOUNTED = 'Y'
               MOVE 'Y' TO FUNCTION-OK
           ELSE
               MOVE 'N' TO FUNCTION-OK
           END-IF.

       START-FIRMWARE.
           DISPLAY WS-JUMP-MESSAGE.
