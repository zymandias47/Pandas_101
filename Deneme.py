import pandas as pd
import matplotlib.pyplot as plt

class Credi_card:

    def __init__(self,file):
        self.data = pd.read_csv(file)
        self.df = pd.DataFrame(self.data)
        self.new_data = None
        self.new_df = None
        self.fig = plt.figure()
        self.subset = pd.DataFrame()
    def card_Type(self):
        #Draws a graph of expenses according to card types
        total= self.df.groupby("Card Type")["Amount"].sum()/1000000
        x1= self.fig.add_subplot(2,2,1)
        x1.set_xticks(range(len(self.df.groupby("Card Type"))))

        x1.plot(total,"r.--")
        x1.set_title("Spending by Cards")
        x1.set_ylabel("Amount(*1M)")
        x1.set_xticklabels(["Gold","Platinum","Signature","Silver"],rotation=60)

    def data_editing(self):
        #Edits the data removes India from the City column and creates a new csv file
        self.data["City"] =self.data["City"].str.replace(", India", "")
        self.data.to_csv("dataset_changed.csv", index=False)
        self.new_data = pd.read_csv("dataset_changed.csv")
        self.new_df = pd.DataFrame(self.new_data)

    def best_cities(self):
        #Draws a graph showing cities with the highest average spending
        cities = self.new_df.groupby("City")["Amount"].mean().sort_values()/100
        best = cities.tail(10)

        x2 = self.fig.add_subplot(2,2,2)
        x2.plot(best,"b.--")
        x2.set_xticks(range(10))
        x2.set_xticklabels(["Viramgam","Kadapa","Yadgir","Rewari","Kashipur","Vellore","Manend","Alwar","Nahan","Thodupuz"],rotation = -80)
        x2.set_title("Most indebted provinces")


    def compare_spending(self):
        #Plots chart comparing average spending in Delhi and Bengaluru over 3-month periods
        self.new_df["Date"] = pd.to_datetime(self.new_df["Date"],format="%d-%b-%y")
        start_date = self.new_df["Date"].min()
        end_date = self.new_df["Date"].max()
        data_range = pd.date_range(start_date,end_date,freq="3M")#Divided into 3 month periods

        x3 = self.fig.add_subplot(2, 2, 3)
        subset_delhi = pd.DataFrame()
        subset_Bengaluru= pd.DataFrame()
        average_amounts_delhi = []
        average_amounts_Bengaluru = []

        for i in range(len(data_range)-1):
            start_range = data_range[i]
            end_range =  data_range[i+1]

            self.subset = self.new_df[(self.new_df['Date'] >= start_range) & (self.new_df['Date'] < end_range)]
            subset_delhi = self.subset.groupby("City").get_group("Delhi")
            subset_Bengaluru = self.subset.groupby("City").get_group("Bengaluru")
            average_amounts_delhi.append(subset_delhi['Amount'].mean()/1000)
            average_amounts_Bengaluru.append(subset_Bengaluru['Amount'].mean() / 1000)

        x3.plot(data_range[:-1], average_amounts_delhi, "g.--",label = "Delhi")
        x3.plot(data_range[:-1], average_amounts_Bengaluru, "r.--", label="Bengaluru")
        x3.legend(loc = "best")
        x3.tick_params(axis="x", rotation=80)

    def ploting(self):
        #Shows all created charts
        plt.tight_layout() #centers the figures in the best position
        plt.show()

credi_cart = Credi_card("Credit card transactions - India - Simple.csv")

credi_cart.card_Type()
credi_cart.data_editing()
credi_cart.best_cities()
credi_cart.compare_spending()
credi_cart.ploting()
