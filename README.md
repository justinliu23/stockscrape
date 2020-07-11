# Stock Tracker

* **Personalize a clipboard of stocks to track via CSV control files** with 3 steps:
  1. Create a CSV file to keep track of your stocks
  2. Refer to `Stocks Clipboard.csv` and only personalize your stocks (case-insensitve), ranges (percent signs optional), and buying prices (dollar signs optional); empty values will be ignored and marked as N/A
  3. Open `tracker.py` and insert the file paths of your stocks clipboard, temporary stocks clipboard (required for updating the clipboard), and email information where designated at lines 14, 15, and 16, respectively
  
* **Receive notifying emails if a stock's buying price falls or rises over a range** with 4 steps:
  1. Enable [Google 2-Step Verification](https://support.google.com/accounts/answer/185839?co=GENIE.Platform%3DAndroid&hl=en)
  2. Generate a [Google App Password](https://support.google.com/accounts/answer/185833?hl=en) for your Gmail account
  3. Create a CSV file to store your email information
  4. Insert your email info and Gmail App Password where designated (refer to `Notifying Email Accounts.csv`)
  
* **Run `main.py`** after you've properly personalized your CSV control files and setup your Gmail Account

* **Automate `main.py` to notify you via email** with 2 steps:
  1. [Convert](https://www.youtube.com/watch?v=UZX5kH72Yx4&list=LLn2A3GlJT_vthodJ8G63-gA&index=3&t=303s) your python script to an executable file
  2. Open Windows Task Scheduler to [schedule a new task](https://windowsreport.com/schedule-tasks-windows-10/) with the generated EXE file in the Actions tab - scheduling other parts of the task are based on personal preferences
