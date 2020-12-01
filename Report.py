import boto3
import smtplib
import pandas as pd
from time import strftime
from extData.sele_v2 import dataExt
from em.ol.olProps import olProps_var
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from aws.meyita.props.pgprodConProps import pgprod_prop




class morningPending():
    def __init__(self):
        # connection string reference to rds
        con = pgprod_prop()
        # Query determines the hight of pending loans right before funding occurs
        qry_Pend = """
            select 
                pd,
                cntformer,
                sumformer,
                cntnewdm,
                sumnewdm,
                cntnew,
                sumnew,
                cnttotal,
                sumtotal
            FROM <table>
            WHERE sumtotal = (
                  SELECT DISTINCT
                    max(sumtotal) 
                  FROM <table name> 
                  WHERE pd = current_date 
                  --WHERE pd = '2019-01-29'  
                    AND ph in (4,5,6,7))
              AND pd = current_date;
        """
        # pandas dataframe
        df_Pend = pd.read_sql_query(qry_Pend, con.pgprodcon)
        df_Pend = df_Pend.drop_duplicates()

        self.cntFormer = format(int(df_Pend['cntformer']), ',')
        self.revFormerTotal = format(int(df_Pend['sumformer']), ',')

        self.cnt_new_dm_Total = format(int(df_Pend['cntnewdm']), ',')
        self.revNew_dm_Total = format(int(df_Pend['sumnewdm']), ',')

        self.cntNewTotal = format(int(df_Pend['cntnew']), ',')
        self.revNewTotal = format(int(df_Pend['sumnew']), ',')

        self.cntTotal = format(int(df_Pend['cnttotal']), ',')
        self.revFundedTotal = format(int(df_Pend['sumtotal']), ',')
        self.calcPendingTotal = int(df_Pend['sumtotal'])
def mornPending_var():
    return mornPending()
# Get, Set CVF from previous day
class mornCVF():
    # if the value of CVF is null or an error then it will auto assign $50,000
    def __init__(self):
        # connection string reference to rds
        con = pgprod_prop()
        # Retrieves the cvf from the previous night
        qry_mornCVF = """
            select ulday, sumh from <table name> where ulday = current_date - 1;
        """
        # pandas dataframe
        df_mornCVF = pd.read_sql_query(qry_mornCVF, con=con.pgprodcon)
        df_mornCVF = df_mornCVF.drop_duplicates()
        try:
            blankIndex = [''] * len(df_mornCVF)
            df_mornCVF.index = blankIndex
            self.sumH = df_mornCVF['sumh'].astype(float)
        except Exception as e:
            print("CVF calculation error: " + str(e))
            self.sumH = float(50000)
def mornCVF_var():
    return mornCVF()
# Get, Set 4 am added loans sumtotal from previous day
class morn4amloansTotal():
    def __init__(self):
        # Retrieves the 4 am added loans
        con = pgprod_prop()
        qry_4amloans = """select max(sumtotal) as sumtotal from <table name>s where pd = current_date"""
        fourDF = pd.read_sql_query(sql=qry_4amloans, con=con.pgprodcon)
        fourDF = fourDF.drop_duplicates()
        try:
            blankIndex = [''] * len(fourDF)
            fourDF.index = blankIndex
            self.fourAMAddedLoansSumtotal = fourDF['sumtotal']
        except Exception as e:
            print("4 am clac error: " + str(e))
        #print(fourDF['sumtotal'])
def morn4amloansTotal_var():
    return morn4amloansTotal()
# Get, Set 5 am added loans sumtotal from previous day
class morn5amloansTotal():
    def __init__(self):
        # Retrieves the 5 am added loans
        con = pgprod_prop()
        qry_5amloans = """select max(sumtotal) as sumtotal from <table name> where pd = current_date"""
        fiveDF = pd.read_sql_query(sql=qry_5amloans, con=con.pgprodcon)
        fiveDF = fiveDF.drop_duplicates()
        try:
            blankIndex = [''] * len(fiveDF)
            fiveDF.index = blankIndex
            self.fiveAMAddedLoansSumtotal = fiveDF['sumtotal']
        except Exception as e:
            print("5 am clac error: " + str(e))
def morn5amloansTotal_var():
    return morn5amloansTotal()
# Get, Set 6 am added loans sumtotal from previous day
class morn6amloansTotal():
    def __init__(self):
        # Retrieves the 5 am added loans
        con = pgprod_prop()
        qry_6amloans = """select max(sumtotal) as sumtotal from <table name> where pd = current_date"""
        sixDF = pd.read_sql_query(sql=qry_6amloans, con=con.pgprodcon)
        sixDF = sixDF.drop_duplicates()
        try:
            blankIndex = [''] * len(sixDF)
            sixDF.index = blankIndex
            self.sixAMAddedLoansSumtotal = sixDF['sumtotal']
        except Exception as e:
            print("6 am clac error: " + str(e))
def morn6amloansTotal_var():
    return morn6amloansTotal()
# download raw and upload aggrigates to rds
def morn4amLoansDLUL():
    dataExt(turl=["Loan_Search2","exit"])
    #print('Starting morning forecast')
    var = pgprod_prop()
    con = var.pgprodcon
    cursor = con.cursor()
    try:
        cd = strftime("%m/%d/%Y")
        tr = cd + ' 04'
        lsRaw = "<file path>"
        df = pd.read_csv("<file path>",
                         index_col='Loan#')

        df['Loan Amount'] = df[df.columns[10]].replace('[\$,]', '', regex=True).astype(float)
        newLoans = df[df['Loan Date/Time'].str.contains(tr)].sum().fillna(0)['Loan Amount']
        lsCalc = newLoans
        qryrf = """
            INSERT INTO
                <table name> (pd,sumtotal)
            VALUES (current_date,""" + str(lsCalc) + """)
        """
        cursor.execute(qryrf)
        con.commit()
        cursor.close()
        con.close()
    except Exception as e:
        #print("4 am Loans failed: " + str(e))
        try:
            day = strftime("%d")
            month = strftime("%m")
            year = strftime("%Y")
            date = year + "-" + month + "-" + day
            lsCalce = int(0)
            qryrf = """
                    INSERT INTO
                        <table name> (pd,sumtotal)
                    VALUES (current_date,""" + str(lsCalce) + """)
                """
            cursor.execute(qryrf)
            con.commit()
            cursor.close()
            con.close()
        except Exception as e:
            print("Back up 4 am Loans failed: " + str(e))
def morn5amLoansDLUL():
    dataExt(turl=["Loan_Search2","exit"])
    #print('Starting morning forecast')
    var = pgprod_prop()
    con = var.pgprodcon
    cursor = con.cursor()
    try:
        cd = strftime("%m/%d/%Y")
        tr = cd + ' 05'
        lsRaw = "C<file path>"
        df = pd.read_csv("<file path>",
                         index_col='Loan#')

        df['Loan Amount'] = df[df.columns[10]].replace('[\$,]', '', regex=True).astype(float)
        newLoans = df[df['Loan Date/Time'].str.contains(tr)].sum().fillna(0)['Loan Amount']
        lsCalc = newLoans
        #print(lsCalc)
        qryrf = """
            INSERT INTO
                <table name> (pd,sumtotal)
            VALUES (current_date,""" + str(lsCalc) + """)
        """
        cursor.execute(qryrf)
        con.commit()
        cursor.close()
        con.close()
    except Exception as e:
        print("5 am Loans failed: " + str(e))
        try:
            day = strftime("%d")
            month = strftime("%m")
            year = strftime("%Y")
            date = year + "-" + month + "-" + day
            lsCalce = int(0)
            qryrf = """
                    INSERT INTO
                        <table name> (pd,sumtotal)
                    VALUES (current_date,""" + str(lsCalce) + """)
                """
            cursor.execute(qryrf)
            con.commit()
            cursor.close()
            con.close()
        except Exception as e:
            print("Back up 5 am Loans failed: " + str(e))
def morn6amLoansDLUL():
    dataExt(turl=["Loan_Search2","exit"])
    #print('Starting morning forecast')
    var = pgprod_prop()
    con = var.pgprodcon
    cursor = con.cursor()
    try:
        cd = strftime("%m/%d/%Y")
        tr = cd + ' 06'
        lsRaw = "<csv file location>"
        df = pd.read_csv("<csv file location>",
                         index_col='Loan#')

        df['Loan Amount'] = df[df.columns[10]].replace('[\$,]', '', regex=True).astype(float)
        newLoans = df[df['Loan Date/Time'].str.contains(tr)].sum().fillna(0)['Loan Amount']
        lsCalc = newLoans
        #print(lsCalc)
        qryrf = """
            INSERT INTO
                <table name> (pd,sumtotal)
            VALUES (current_date,""" + str(lsCalc) + """)
        """
        cursor.execute(qryrf)
        con.commit()
        cursor.close()
        con.close()
    except Exception as e:
        print("6 am Loans failed: " + str(e))
        try:
            day = strftime("%d")
            month = strftime("%m")
            year = strftime("%Y")
            date = year + "-" + month + "-" + day
            lsCalce = int(0)
            qryrf = """
                    INSERT INTO
                        <table name> (pd,sumtotal)
                    VALUES (current_date,""" + str(lsCalce) + """)
                """
            cursor.execute(qryrf)
            con.commit()
            cursor.close()
            con.close()
        except Exception as e:
            print("Back up 6 am Loans failed: " + str(e))
# Morning Forecast Calculation
class mornForecastCalc():
    def __init__(self):
        #print("Start Morning Forecast")
        if morn4amloansTotal_var().fourAMAddedLoansSumtotal is None :
            addL4 = 0
        else:
            addL4 = morn4amloansTotal_var().fourAMAddedLoansSumtotal
        if morn5amloansTotal_var().fiveAMAddedLoansSumtotal is None:
            addL5 = 0
        else:
            addL5 = morn5amloansTotal_var().fiveAMAddedLoansSumtotal
        if morn6amloansTotal_var().sixAMAddedLoansSumtotal is None:
            addL6 = 0
        else:
            addL6 = morn6amloansTotal_var().sixAMAddedLoansSumtotal
        cvf = mornCVF_var().sumH
        mp = mornPending_var().calcPendingTotal
        #print("4 am added loans: " + str(addL4))
        #print("5 am added loans: " + str(addL5))
        #print("6 am added loans: " + str(addL6))
        #print("CVF total: " + str(cvf))
        #print("Pending total: " + str(mp))
        addedLoans = [addL4, addL5, addL6]
        hrR = max(addedLoans, key=lambda item:item[0])
        print('Loans Added per Hour')
        print(hrR)
        totalHrR = hrR * 8
        print('Total loans per hour')
        print(totalHrR)
        print('cfv')
        print(cvf)
        #print("added by hour: " + str(hrR))
        self.morningFundingForecast = ((hrR * 8) + mp) + cvf
        print("morning forecast is: " + str(self.morningFundingForecast))
def mornForecastCalc_var():
    return mornForecastCalc()
# Load Morning Forecast to rds table
def mornforecastUL():
    var = pgprod_prop()
    con = var.pgprodcon
    cursor = con.cursor()
    mf = int(mornForecastCalc_var().morningFundingForecast)
    qryrf = """
        INSERT INTO
            <table name> (pd,mornforecast)
            VALUES (current_date,""" + str(mf) + """)
        """
    cursor.execute(qryrf)
    con.commit()
    cursor.close()
    con.close()
# mornforecast DynamoDB UL
def mornforecastDynamoDBUL():
    cd = strftime("%Y-%m-%d")
    mf = int(mornForecastCalc_var().morningFundingForecast)
    sesh = boto3.Session()
    dynamodb = sesh.resource('dynamodb', region_name="us-east-2")
    table = dynamodb.Table('<table name>')
    table.put_item(
        Item={
            "uldate":cd,
            "mornforecast": mf
        }
    )
    print("Successfully updated mornforecast table in dynamoDB")
# risk forecast
class mornRiskCalc():
    def __init__(self):
        con = pgprod_prop()
        print('initiating risk forecast')
        qry_rf = """
            SELECT
                *
            FROM <table name>
            WHERE CAST(fdate as date) = current_date;
        """
        # risk forecast
        rfDF = pd.read_sql_query(qry_rf, con.pgprodcon)
        self.rfTotal = format(int(rfDF['ftotal']), ',')
        #print('rftotal')
        print(self.rfTotal)
def mornRiskCalc_var():
    return mornRiskCalc()
# email report
def morningFundingReportEM():
    msg = MIMEMultipart()
    recpSolo = ["<Your email>"]
    recpTest = ["<your test distro>"]
    recp = ["<your distro list>"]
    sender = "<your email address>"
    msg['To'] = ", ".join(recpSolo)
    msg['From'] = sender
    msg['Subject'] = "<your subject line>"

    bodyORG = MIMEText(""" 
               <html>You HTML for the email.</html>
                """, 'html', 'utf-8')

    msg.attach(bodyORG)
    olp = olProps_var()
    s = smtpserver = smtplib.SMTP("smtp-mail.outlook.com", 587)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.login(olp.MSUS, olp.MSPS)
    s.sendmail(sender, recpSolo, msg.as_string())
    print('done!')
    s.close()


