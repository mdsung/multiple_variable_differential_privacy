import numpy as np
class ApacheIV:
    def __init__(self, series):
        self.apache_score = {}
        self.calculate_temperature(series.temperature)
        self.calculate_meanbp(series.meanbp)
        self.calculate_heartrate(series.heartrate)
        self.calculate_respiratoryrate(series.respiratoryrate)
        self.calculate_acid(series.ph, series.pco2)
        self.calculate_sodium(series.sodium)
        self.calculate_urine(series.urine)
        self.calculate_creatinine(series.creatinine, series.urine, series.dialysis)
        self.calculate_bun(series.bun)
        self.calculate_glucose(series.glucose)
        self.calculate_albumin(series.albumin)
        self.calculate_bilirubin(series.bilirubin)
        self.calculate_hematocrit(series.hematocrit)
        self.calculate_wbc(series.wbc)
        self.calculate_gcs(series.meds, series.eyes, series.motor, series.verbal)
        self.calculate_oxygenation(series.vent, series.pao2, series.pco2, series.fio2)
        self.calculate_apache_iv()
    
    def calculate_temperature(self, temperature):

        score = 0
        if np.isnan(temperature):
            self.apache_score["temperature"] = 0
            return

        if temperature < 33:
            score += 20
        elif temperature < 33.5:
            score += 16
        elif temperature < 34:
            score += 13
        elif temperature < 35:
            score += 8
        elif temperature < 36:
            score += 2
        elif temperature < 40:
            score += 0
        else:
            score += 4
        
        self.apache_score["temperature"] = score

    def calculate_meanbp(self, meanbp):
        score = 0
        if np.isnan(meanbp):
            self.apache_score["meanbp"] = 0
            return
    
        if meanbp <= 39:
            score += 23
        elif meanbp < 60:
            score += 15
        elif meanbp < 70:
            score += 7
        elif meanbp < 80:
            score += 6
        elif meanbp < 100:
            score += 0
        elif meanbp < 120:
            score += 4
        elif meanbp < 130:
            score += 7
        elif meanbp < 140:
            score += 9
        else:
            score += 10

        self.apache_score["meanbp"] = score

    def calculate_heartrate(self, heartrate):
        score = 0
        if np.isnan(heartrate):
            self.apache_score["heartrate"] = 0
            return
        if heartrate < 40:
            score += 8
        elif heartrate < 50:
            score += 5
        elif heartrate < 100:
            score += 0
        elif heartrate < 110:
            score += 1
        elif heartrate < 120:
            score += 5
        elif heartrate < 140:
            score += 7
        elif heartrate < 155:
            score += 13
        else:
            score += 17
        self.apache_score["heartrate"] = score

    def calculate_respiratoryrate(self, respiratoryrate):
        score = 0
        if np.isnan(respiratoryrate):
            self.apache_score["respiratoryrate"] = 0
            return
        if respiratoryrate <= 5:
            score += 1
        elif respiratoryrate < 12:
            score += 8
        elif respiratoryrate < 14:
            score += 7
        elif respiratoryrate < 25:
            score += 0
        elif respiratoryrate < 35:
            score += 6
        elif respiratoryrate < 40:
            score += 9
        elif respiratoryrate < 50:
            score += 1
        else: 
            score += 18

        self.apache_score["respiratoryrate"] = score

    def calculate_acid(self, ph, pco2):
        score = 0
        if np.isnan(ph) | np.isnan(pco2):
            self.apache_score["acid"] = score
            return 

        if ph < 7.2:
            if pco2 < 50:
                score += 12
            else:
                score += 4

        elif ph < 7.3:
            if pco2 < 30:
                score += 9
            elif pco2 < 40:
                score += 6
            elif pco2 < 50:
                score += 3
            else:
                score += 2

        elif ph < 7.35:
            if pco2 < 30:
                score += 9
            elif pco2 < 45:
                score += 0
            else:
                score += 1

        elif ph < 7.45:
            if pco2 < 30 :
                score += 5    
            elif pco2 < 45:
                score += 0
            else :
                score += 1

        elif ph < 7.5:
            if pco2< 30:
                score += 5
            elif pco2< 35:
                score += 0
            elif pco2< 45:
                score += 2
            else:
                score += 12

        elif ph < 7.6:
            if pco2 < 40:
                score += 3
            else:
                score += 12
        else:
            if pco2 < 25:
                score += 0
            if pco2 < 40:
                score += 3
            else:
                score += 12

        self.apache_score["acid"] = score

    def calculate_sodium(self, sodium):
        score = 0 
        if np.isnan(sodium):
            self.apache_score["sodium"] = 0
            return
        if (sodium < 120):
            score += 3
        elif (sodium < 135):
            score += 2
        elif (sodium < 155):
            score += 0
        else:
            score += 4

        self.apache_score["sodium"] = score

    def calculate_urine(self, urine):
        score = 0
        if np.isnan(urine):
            self.apache_score["urine"] = score
            return

        if (urine < 400):
            score += 15
        elif (urine < 600):
            score += 8
        elif (urine < 900):
            score += 7
        elif (urine < 1500):
            score += 5
        elif (urine < 2000):
            score += 4
        elif (urine < 4000):
            score += 0
        else:
            score += 1
        self.apache_score["urine"] = score

    def calculate_creatinine(self, creatinine, urine, dialysis):
        score = 0
        if np.isnan(creatinine):
            self.apache_score["creatinine"] = 0
            return

        if dialysis == 0:
            if (urine < 410) & (creatinine >= 1.5):
                score += 10
            else:
                if (creatinine < 0.5):
                    score += 3
                elif (creatinine < 1.5):
                    score += 0
                elif (creatinine < 1.95):
                    score += 4
                else:
                    score += 7

        if dialysis == 1:
            if creatinine < 0.5:
                score += 3
            elif (creatinine < 1.5):
                score += 0
            elif (creatinine < 1.95):
                score += 4
            else:
                score += 7

        self.apache_score["creatinine"] = score

    def calculate_bun(self, bun):
        score = 0
        if (bun < 17):
            score += 0
        elif (bun < 20):
            score += 2
        elif (bun < 40):
            score += 7
        elif (bun < 80):
            score += 11
        else:
            score += 12
        
        self.apache_score["bun"] = score

    def calculate_glucose(self, glucose):
        score = 0 
        if np.isnan(glucose):
            self.apache_score["glucose"] = 0
            return
        if (glucose < 40):
            score += 8
        elif (glucose < 60):
            score += 9
        elif (glucose < 200):
            score += 0
        elif (glucose < 350):
            score += 3
        else:
            score += 5

        self.apache_score["glucose"] = score

    def calculate_albumin(self, albumin):
        score = 0
        if np.isnan(albumin):
            self.apache_score["albumin"] = 0
            return
        if (albumin < 2.0):
            score += 11
        elif albumin < 2.5:
            score += 6
        elif (albumin < 4.5):
            score += 0
        else:
            score += 4
        self.apache_score["albumin"] = score

    def calculate_bilirubin(self, bilirubin):
        score = 0 
        if np.isnan(bilirubin):
            self.apache_score["bilirubin"] = 0
            return
        if bilirubin < 2:
            score += 0
        elif bilirubin < 3:
            score += 5
        elif bilirubin < 5:
            score += 6
        elif bilirubin < 8:
            score += 8
        else:
            score += 16
        
        self.apache_score["bilirubin"] = score
        
    def calculate_hematocrit(self, hematocrit):
        score = 0
        if np.isnan(hematocrit):
            self.apache_score["hematocrit"] = 0
            return
        if (hematocrit < 41):
            score += 3
        elif (hematocrit < 50):
            score += 0
        else:
            score += 3

        self.apache_score["hematocrit"] = score

    def calculate_wbc(self, wbc):
        score = 0
        if np.isnan(wbc):
            self.apache_score["wbc"] = 0
            return
        if (wbc < 1):
            score += 19
        elif (wbc < 3):
            score += 5
        elif (wbc < 20):
            score += 0
        elif (wbc < 25):
            score += 1
        else:
            score += 5
        self.apache_score["wbc"] = score

    def calculate_gcs(self, medications, gce, gcm, gcv):
        score = 0
        if np.isnan(gce) |np.isnan(gcm)|np.isnan(gcv):
            self.apache_score["gcs"] = 0
            return

        if (medications == 1):
            score += 0
        
        if (medications == 0):
            if (gce == 1):
                if 5 <= gcm <=6:
                    if gcv == 1:
                        score += 16

                if 3 <= gcm <= 4:
                    if 2 <= gcv <= 3:
                        score += 24
                    if gcv == 1:
                        score += 3
            if 1 <= gcm <= 2:
                if 2 <= gcv <= 3:
                    score += 29
                if gcv == 1:
                    score += 48
    
            elif (gce != 1):  
                if (gcm == 6):  
                    if gcv == 5:  
                        score += 0
                    if gcv == 4:
                        score += 3
                    if 2 <= gcv <= 3:
                        score += 10
                    if gcv == 1:
                        score += 15

                if (gcm == 5):  
                    if (gcv == 5):
                        score += 3
                    if (gcv == 4):
                        score += 8
                    if 2<= gcv <=3:
                        score += 13
                    if (gcv == 1):
                        score += 15
                    
                if 3<= gcm <=4:
                    if (gcv == 5):
                        score += 3
                    if (gcv == 4):
                        score += 13
                    if 1<= gcv <= 3 :
                        score += 24

                if 1 <= gcm <= 2:
                    if gcv == 5:
                        score += 3
                    if gcv == 4:
                        score += 13
                    if 1<= gcv <=3 :
                        score += 29

        self.apache_score["gcs"] = score

    def calculate_oxygenation(self, ventilator, pao2, paco2, fio2):
        score = 0
        patm = 760
        aado2 = (fio2/100)*(patm-47)-(paco2/0.8)-pao2

        if np.isnan(pao2):
            self.apache_score["pao2"] = 0
            return
        
        if ventilator == 0:
            if (pao2 < 50):
                score += 15
            elif (pao2 < 70):
                score += 5
            elif (pao2 < 80):
                score += 2
            else:
                score += 0

        if ventilator == 1:
            if (fio2 >= 50):
                if (aado2 < 100):
                    score += 0
                elif (aado2 < 250):
                    score += 7
                elif (aado2 < 350):
                    score += 9
                elif (aado2 < 500):
                    score += 11
                else:
                    score += 14

            if (fio2 < 50):
                if (pao2 < 50):
                    score += 15
                elif (pao2 < 70):
                    score += 5
                elif (pao2 < 80):
                    score += 2
                else:
                    score += 0

        self.apache_score["oxygenation"] = score

    def calculate_apache_iv(self):
        return sum(self.apache_score.values())




    

    

