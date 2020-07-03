# Stock Manager

* Personalize a clipboard of stocks to track based on [Yahoo! Finance](https://finance.yahoo.com/) with 2 steps:
  1. Create a CSV file (Excel recommended), label it "Stocks Clipboard.csv", and format it like so: [Stocks Clipboard.csv](C:\Users\justi\OneDrive\Documents\Software\Python\PycharmProjects\Price Checkers\Stocks\stock-tracker\Stocks Clipboard Example.PNG)
  2. Generate a [Google App Password](https://support.google.com/accounts/answer/185833?hl=en) for your Gmail account
  3. Change the sample email addresses (someone@example.com) to your email
  4. Insert your generated Gmail App Password where it says, "Insert your generated Gmail App Password here"

* Notifies you via email if a stock on your clipboard falls or rises over 5% of your buying price

* Receiving emails requires 4 simple steps:
  1. Enable [Google 2-Step Verification](https://support.google.com/accounts/answer/185839?co=GENIE.Platform%3DAndroid&hl=en)
  2. Generate a [Google App Password](https://support.google.com/accounts/answer/185833?hl=en) for your Gmail account
  3. Change the sample email addresses (someone@example.com) to your email
  4. Insert your generated Gmail App Password where it says, "Insert your generated Gmail App Password here"
  
* Run `main.py` after you personalize your email login information and clipboard of stocks to use

* Automating `main.py` to notify you via email requires 2 steps:
  1. [Convert](https://www.youtube.com/watch?v=UZX5kH72Yx4&list=LLn2A3GlJT_vthodJ8G63-gA&index=3&t=303s) your python script (.py) to an executable file (.exe)
  2. Open Windows Task Scheduler to [schedule a new task](https://windowsreport.com/schedule-tasks-windows-10/) with the generated .exe file in the Actions tab - scheduling other parts of the task are based on personal preferences
