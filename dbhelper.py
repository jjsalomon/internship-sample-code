# -*- coding: utf-8 -*-
import sqlite3

class DatabaseHelper():
    # This class is a singleton instance
    __instance = None
    
    @staticmethod
    def getInstance():
        if DatabaseHelper.__instance == None:
            DatabaseHelper()
        return DatabaseHelper.__instance
    '''Constructor'''
    def __init__(self):
        if DatabaseHelper.__instance != None:
            print("Returning Database Helper Instance")
        else:
            DatabaseHelper.__instance = self
            print('[BOOTING]: Database Helper Module')
            self.create_tables()
        
    # Method to allow for easy connections to the database
    def connect_db(self):
        try:
            conn = sqlite3.connect('database.db',timeout = 10)
            print('[SUCCESS]: Connected to the Database')
            return conn
        except Exception as e:
            print("[FAIL]: Could not connect to the Database")
            raise e
            
    def create_tables(self):
        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute('''
                           CREATE TABLE IF NOT EXISTS users(ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                                            username VARCHAR(20) NOT NULL UNIQUE,
                                                            password VARCHAR(20) NOT NULL,
                                                            sex VARCHAR(10) NOT NULL,
                                                            age int,
                                                            diagnosed int)
                           ''')
            cursor.execute('''
                           CREATE TABLE IF NOT EXISTS audio_recordings(ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                                                       accuracypercentage float NOT NULL, 
                                                                       pitch_variance float NOT NULL,
                                                                       wordspermin float NOT NULL,
                                                                       modal_frequency float NOT NULL, 
                                                                       breath_time float NOT NULL,
                                                                       avg_amplitude float NOT NULL,
                                                                       filename text NOT NULL,
                                                                       userID int,
                                                                       FOREIGN KEY (userID) REFERENCES users(ID)
                                                                       )
                           ''')
            cursor.execute('''
                           CREATE TABLE IF NOT EXISTS prescreening(ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                                                   recordID int,
                                                                   mood VARCHAR(10) NOT NULL,
                                                                   medication VARCHAR(10) NOT NULL,
                                                                   food VARCHAR(10),
                                                                   FOREIGN KEY(recordID) REFERENCES users(ID)
                                                                   )
                          ''')
            cursor.execute('''
                           CREATE TABLE IF NOT EXISTS config(ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                                                   recordID int,
                                                                   time INTEGER NOT NULL,
                                                                   ch_acc INTEGER NOT NULL,
                                                                   ch_wpm INTEGER,
                                                                   ch_freq INTEGER,
                                                                   ch_mod_freq INTEGER,
                                                                   ch_avg_amp INTEGER,
                                                                   ch_breath INTEGER,
                                                                   FOREIGN KEY(recordID) REFERENCES users(ID)
                                                                   )
                          ''')
            cursor.execute('''
                           CREATE TABLE IF NOT EXISTS video_recordings(ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                                                           recordID int NOT NULL,
                                                                           total_blinks int NOT NULL,
                                                                           total_peaks int NOT NULL,
                                                                           total_troughs int 
                                                                           blinkspermin float NOT NULL,
                                                                           peakspermin float NOT NULL,
                                                                           troughspermin float NOT NULL,
                                                                           video_duration float NOT NULL,
                                                                           FOREIGN KEY(recordID) REFERENCES users(ID))
                           ''')

            conn.commit()
            print("[SUCCESS]: Created the tables")
        except Exception as e:
            print("[FAIL]: Could not create tables")
            raise e
            conn.rollback()
        finally:
            conn.close()
        
    def insert_users(self,username,password,sex,age,diagnosed,case):
        try:
            conn = self.connect_db()
            #conn = sqlite3.connect('database.db',timeout = 10)
            cursor = conn.cursor()
            cursor.execute('''
                           INSERT INTO users(username,password,sex,age,diagnosed) VALUES(?,?,?,?,?)
                           ''', (username,password,sex,age,diagnosed))
            print('[SUCCESS]: Inserted a user')
            if(case == "Testing"):
                conn.rollback()
                return
            else:
                conn.commit()
        except Exception as e:
            print("[FAIL]: Failed to insert the user into DB")
            raise e
            conn.rollback()
        finally:
            conn.close()
            
    def insert_audiorecordings(self,userId,accuracypercent,filename,wpm,pitch_var,mfreq,breath_time,avgAmp,case):
        try:
            conn = self.connect_db()
            #conn = sqlite3.connect('database.db',timeout = 10)
            # INSERT VALUES
            cursor = conn.cursor()
            cursor.execute('''
                           INSERT INTO audio_recordings(accuracypercentage,filename,pitch_variance,wordspermin,modal_frequency, breath_time, avg_amplitude,userID)
                           VALUES(?,?,?,?,?,?,?,?)''',(accuracypercent,filename,pitch_var,wpm,mfreq,breath_time,avgAmp,userId))
            if(case == "Testing"):
                conn.rollback()
                return
            else:
                conn.commit()
        except Exception as e:
            print("[FAIL]: Failed to insert recordings into DB")
            raise e
            conn.rollback()
        finally:
            conn.close()
            
    def insert_videorecordings(self,userId,blinks,peaks,troughs,blinkspermin,peakspermin,troughspermin,duration,case):
        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute('''
                           INSERT INTO video_recordings(recordID,total_blinks,total_peaks,total_troughs,blinkspermin,
                                                        peakspermin,troughspermin,video_duration) VALUES(?,?,?,?,?,?,?,?)
                           ''',(userId,blinks,peaks,troughs,blinkspermin,peakspermin,troughspermin,duration))
            if(case == "Testing"):
                conn.rollback()
                return
            else:
                conn.commit()
        except Exception as e:
            print("[FAIL]: Failed to insert video recordings into DB")
            raise e
            conn.rollback()
        finally:
            conn.close()
            
    def insert_prescreening(self, mood,medication,food,userId,case):
        try:
            conn = self.connect_db()
            #conn = sqlite3.connect('database.db',timeout = 10)
            cursor = conn.cursor()
            cursor.execute('''
                           INSERT INTO prescreening(recordID,mood,medication,food) 
                           VALUES(?,?,?,?)''',(userId,mood,medication,food))
            print('[SUCCESS]: Inserted prescreening')
            if(case == "Testing"):
                conn.rollback()
                return
            else:
                conn.commit()
        except Exception as e:
            print('[FAIL]: Failed to insert a text sample into the DB')
            raise e
            conn.rollback()
        finally:
            conn.close()
            
    def insert_config(self,userId,time,ch_acc,ch_wpm,ch_freq,ch_mod_freq,ch_breath,ch_avg_amp,case):
        try:
            conn = self.connect_db()
            #conn = sqlite3.connect('database.db',timeout = 10)
            cursor = conn.cursor()
            cursor.execute('''
                           INSERT INTO config(recordID,time,ch_acc,ch_wpm,ch_freq,ch_mod_freq,ch_breath,ch_avg_amp)
                           VALUES(?,?,?,?,?,?,?,?)''',(userId,time,ch_acc,ch_wpm,ch_freq,ch_mod_freq,ch_breath,ch_avg_amp))
            print('[SUCCESS]: Inserted config')
            if(case == "Testing"):
                conn.rollback()
                return
            else:
                conn.commit()
        except Exception as e:
            print('[FAIL]: Failed to insert a text sample into the DB')
            raise e
            conn.rollback()
        finally:
            conn.close()   
            
            
    # SELECT function to return values
    # Placeholder for now
    # But it works
    def return_data(self):
        conn = self.connect_deb()
        #conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        selectcur = cursor.execute('''
                                   SELECT * FROM users''')
        for row in selectcur:
            print('{0} : {1}, {2}'.format(row[0],row[1],row[2]))
            
            
    def checkUserCredentials(self,function,username,password):
        try:
            data = []
            conn = self.connect_db()
            #conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            selectcur = cursor.execute('''
                                       SELECT ID,username FROM users WHERE username = ? AND password = ?''',
                                       (username,password))
            row = selectcur.fetchone()
            # If from Login function
            if(function == 'Login'):
                # Check if user exists
                if row is None:
                    return "Invalid"
                else:
                    for member in row:
                        data.append(member)
                    # Check if the form username is the same as the Database
                    if(username == data[1]):
                        # Return the user ID at user table
                        return data[0]
                    else:
                        return 'Invalid'
            # Else if from Register function
            elif(function == 'Register'):
                if row is None:
                    return "Valid"
                else:
                    # User already exists in the Database
                    return "Invalid"
        except Exception as e:
            print('[FAIL]: Failed to perform check function - DB error')
            raise e
            conn.rollback()
        finally:
            conn.close()
    
    def return_audiorecordings(self,userId):
        try:
            conn = self.connect_db()
            #conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            selectcur = cursor.execute('''
                                       SELECT accuracypercentage, filename, pitch_variance,wordspermin,modal_frequency, breath_time, avg_amplitude FROM audio_recordings 
                                       WHERE userID = ?
                                       ''',(userId,))
            # This took me ages.....
            row = selectcur.fetchall()
            acc = []
            fn = []
            pitch_var = []
            wpm = []
            mFreq = []
            brTime = []
            avgAmp = []
            for i in row:
                acc.append(i[0])
                fn.append(i[1])
                pitch_var.append(i[2])
                wpm.append(i[3])
                mFreq.append(i[4])
                brTime.append(i[5])
                avgAmp.append(i[6])
                
            return acc, fn, wpm, pitch_var,mFreq,brTime,avgAmp
        except Exception as e:
            print('[FAIL]: Failed to return audio recordings- DB error')
            raise e
            conn.rollback()
        finally:
            conn.close()
    
    def return_config(self,userID):
        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            selectcur = cursor.execute('''
                                       SELECT ch_acc, ch_wpm, ch_freq, ch_mod_freq,ch_breath,ch_avg_amp FROM config 
                                       WHERE recordID = ?
                                       ''',(userID,))
            row = selectcur.fetchall()
            acc = []
            pitch_var = []
            wpm = []
            mFreq = []
            brTime = []
            avgAmp = []
            for i in row:
                acc.append(i[0])
                pitch_var.append(i[1])
                wpm.append(i[2])
                mFreq.append(i[3])
                brTime.append(i[4])
                avgAmp.append(i[5])
                
            try:
                return acc,pitch_var,wpm,mFreq,brTime,avgAmp
            except IndexError:
                return None,None,None,None,None,None
        except Exception as e:
            print('[FAIL]: Failed to return config settings- DB error')
            raise e
            conn.rollback()
        finally:
            conn.close()
            
    