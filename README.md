# Stock Tracker

* **Personalize a clipboard of stocks to track** based on [Yahoo! Finance](https://finance.yahoo.com/) with 4 steps:
  1. ###### Create a **CSV** file to serve as your stocks clipboard and when personalizing your stocks info (**Excel recommended**), refer to `Stocks Clipboard.csv`
  2. ###### Create a **CSV** file to store your notifying email accounts and when personalizing your email info (**Excel recommended**), refer to `Notifying Email Accounts.csv`
  3. Open tracker.py and insert the file path of your stocks clipboard CSV file with directories seperated by **'\\\\'** (ex. *C:\\\\Users\\\\John\\\\Stocks Clipboard.csv*) where designated at line 10
  4. Open `tracker.py` and insert the file path of your notifying email accounts CSV file with directories seperated by **'\\\\'** (ex. *C:\\\\Users\\\\John\\\\Notifying Email Accounts.csv*) where designated at line 13

* **Receive notifying emails** if a stock on your clipboard falls or rises over **5%** of your buying price with 4 steps:
  1. Enable [Google 2-Step Verification](https://support.google.com/accounts/answer/185839?co=GENIE.Platform%3DAndroid&hl=en)
  2. Generate a [Google App Password](https://support.google.com/accounts/answer/185833?hl=en) for your Gmail account
  3. Insert your generated Gmail App Password where designated (refer to `Notifying Email Accounts.csv`)
  
* *Run `main.py` after you've properly personalized your CSV control files and setup your Gmail Account*

* Automating `main.py` to notify you via email requires 2 steps:
  1. [Convert](https://www.youtube.com/watch?v=UZX5kH72Yx4&list=LLn2A3GlJT_vthodJ8G63-gA&index=3&t=303s) your python script (.py) to an executable file (.exe)
  2. Open Windows Task Scheduler to [schedule a new task](https://windowsreport.com/schedule-tasks-windows-10/) with the generated EXE file in the Actions tab - scheduling other parts of the task are based on personal preferences
