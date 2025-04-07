IDENTIFICATION DIVISION.
       PROGRAM-ID. SECURITY-BOOT.

       ENVIRONMENT DIVISION.
       INPUT-OUTPUT SECTION.
       FILE-CONTROL.

       DATA DIVISION.
       WORKING-STORAGE SECTION.

       01 WS-MESSAGE         PIC X(20) VALUE "Booting".
       01 WS-LOAD-MESSAGE    PIC X(20) VALUE "Loaded".
       01 WS-ERROR-MESSAGE   PIC X(20) VALUE "Error".
       01 FUNCTION-OK        PIC X     VALUE SPACE.

       PROCEDURE DIVISION.
       MAIN-PROCEDURE.
           DISPLAY WS-MESSAGE.
           PERFORM INITIALIZE-SYSTEM.
           
           IF FUNCTION-OK = 'Y'
               DISPLAY WS-LOAD-MESSAGE
               PERFORM START-FIRMWARE
           ELSE
               DISPLAY WS-ERROR-MESSAGE
           END-IF.

           STOP RUN.

       INITIALIZE-SYSTEM.
           DISPLAY "Setting video mode...".
           DISPLAY "Reading firmware sector...".
           DISPLAY "Setting up paging and segmentation...".
           DISPLAY "USB and Serial Init...".
           DISPLAY "Filesystem Init...".
           MOVE 'Y' TO FUNCTION-OK.

       START-FIRMWARE.
           DISPLAY "Jumping to firmware...".
