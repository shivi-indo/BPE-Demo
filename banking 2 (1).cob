       IDENTIFICATION DIVISION.
       PROGRAM-ID. BANKSYS.

       DATA DIVISION.
       WORKING-STORAGE SECTION.

       01 WS-CHOICE        PIC 9.
       01 WS-BALANCE       PIC 9(7)V99 VALUE 1000.00.
       01 WS-AMOUNT        PIC 9(7)V99.
       01 WS-EXIT          PIC X VALUE 'N'.

       PROCEDURE DIVISION.

       MAIN-PARA.
           PERFORM UNTIL WS-EXIT = 'Y'

               DISPLAY "============================"
               DISPLAY "      SIMPLE BANK SYSTEM    "
               DISPLAY "============================"
               DISPLAY "1. CHECK BALANCE"
               DISPLAY "2. DEPOSIT"
               DISPLAY "3. WITHDRAW"
               DISPLAY "4. EXIT"
               DISPLAY "ENTER YOUR CHOICE: "

               ACCEPT WS-CHOICE

               EVALUATE WS-CHOICE

                   WHEN 1
                       DISPLAY "CURRENT BALANCE: "
                               WS-BALANCE

                   WHEN 2
                       DISPLAY "ENTER DEPOSIT AMOUNT: "
                       ACCEPT WS-AMOUNT
                       ADD WS-AMOUNT TO WS-BALANCE
                       DISPLAY "AMOUNT DEPOSITED SUCCESSFULLY"
                       DISPLAY "UPDATED BALANCE: "
                               WS-BALANCE

                   WHEN 3
                       DISPLAY "ENTER WITHDRAW AMOUNT: "
                       ACCEPT WS-AMOUNT

                       IF WS-AMOUNT > WS-BALANCE
                           DISPLAY "INSUFFICIENT BALANCE"
                       ELSE
                           SUBTRACT WS-AMOUNT
                               FROM WS-BALANCE
                           DISPLAY "WITHDRAW SUCCESSFUL"
                           DISPLAY "UPDATED BALANCE: "
                                   WS-BALANCE
                       END-IF

                   WHEN 4
                       MOVE 'Y' TO WS-EXIT
                       DISPLAY "THANK YOU FOR USING BANKSYS"

                   WHEN OTHER
                       DISPLAY "INVALID OPTION"

               END-EVALUATE

           END-PERFORM.

           STOP RUN.