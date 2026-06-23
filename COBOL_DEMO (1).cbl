       IDENTIFICATION DIVISION.
       PROGRAM-ID. ChequeHandler.

       ENVIRONMENT DIVISION.
       INPUT-OUTPUT SECTION.
       FILE-CONTROL.
           SELECT ACCOUNTS ASSIGN TO 'accounts.dat'
               ORGANIZATION IS LINE SEQUENTIAL.

       DATA DIVISION.
       FILE SECTION.
       FD  ACCOUNTS.
       01  ACCOUNT-RECORD.
           05  ACCOUNT-NUMBER     PIC X(10).
           05  ACCOUNT-HOLDER     PIC X(20).
           05  ACCOUNT-BALANCE    PIC 9(7)V99.

       WORKING-STORAGE SECTION.
       01  WS-CHEQUE.
           05  WS-ACCOUNT-NUM     PIC X(10).
           05  WS-CHEQUE-NUM      PIC X(6).
           05  WS-CHEQUE-AMOUNT   PIC 9(7)V99.

       01  WS-FOUND               PIC X VALUE 'N'.
       01  WS-NEW-BALANCE         PIC 9(7)V99.
       01  EOF-FLAG               PIC X VALUE 'N'.

       01  DISPLAY-MSG            PIC X(80).

       PROCEDURE DIVISION.
       BEGIN.
           DISPLAY "Enter Account Number: " WITH NO ADVANCING
           ACCEPT WS-ACCOUNT-NUM

           DISPLAY "Enter Cheque Number: " WITH NO ADVANCING
           ACCEPT WS-CHEQUE-NUM

           DISPLAY "Enter Cheque Amount: " WITH NO ADVANCING
           ACCEPT WS-CHEQUE-AMOUNT

           OPEN INPUT ACCOUNTS

           PERFORM UNTIL EOF-FLAG = 'Y'
               READ ACCOUNTS
                   AT END
                       MOVE 'Y' TO EOF-FLAG
                   NOT AT END
                       IF ACCOUNT-NUMBER = WS-ACCOUNT-NUM
                           MOVE 'Y' TO WS-FOUND
                           IF ACCOUNT-BALANCE >= WS-CHEQUE-AMOUNT
                               COMPUTE WS-NEW-BALANCE = ACCOUNT-BALANCE - WS-CHEQUE-AMOUNT
                               DISPLAY "Cheque Approved."
                               DISPLAY "New Balance: " WS-NEW-BALANCE
                           ELSE
                               DISPLAY "Insufficient Funds. Cheque Rejected."
                           END-IF
                       END-IF
               END-READ
           END-PERFORM

           IF WS-FOUND = 'N'
               DISPLAY "Account Not Found."
           END-IF

           CLOSE ACCOUNTS

           STOP RUN.
