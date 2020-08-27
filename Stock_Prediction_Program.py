"""This program will allow the user to predict whether a company's stock of their choice will increase or decrease in the future.
They can use the machine learning technique of their choice: Decision Tree, K-Nearest Neighbors, or a Neural Network.
They can also test the model after a technique is built. In addition, they can create a line graph of
a company's historical data of stock change in price over time by a start and end date of their choice."""

import requests
import json
import sklearn.neural_network
import sklearn.tree
import sklearn.neighbors
import sklearn.metrics
import matplotlib.pyplot as plt

print("Hello! Welcome to Brown Sugar's Stock Price Prediction Program!")

repeat = "yes"

while repeat == "yes":
    
    company = input("Please enter the symbol of the company you would like:").upper()
    ml = input("Which maching learning technique would you like to utilize?: (Decision Tree, KNN, Neural Network)").lower()
    while ml.lower() != "decision tree" and ml.lower() != "knn" and ml.lower() != "neural network":
        print("Please enter a valid analysis.")
        ml = input("Which maching learning technique would you like to utilize?: (Decision Tree, KNN, Neural Network)").lower()
    not_closed_input = float(input("Please enter the stock's current open value:"))
    volume_input = float(input("Please enter the stock's current volume value:"))
    visualization = input("Would you also like a visualization of the stock's price change over time?").lower()
    validation = input("Would you like to evaluate the Machine Learning model?")
    
    if visualization == "yes":
        start_date = input("Please input a start date: (YYYY-MM-DD)")
        end_date = input("Please input an end date: (YYYY-MM-DD)")
        

    
    if company:
    
        #response = requests.get("https://sandbox.iexapis.com/stable/stock/"+company+ "/chart/2y?token=Tpk_fa2e8f176abb438caab9817db010c94b") #2 year one
        response = requests.get("https://sandbox.iexapis.com/v1/stock/"+company+"/chart/5y?token=Tpk_fa2e8f176abb438caab9817db010c94b") #5 year one
        #response = requests.get("https://cloud.iexapis.com/stable/stock/"+company+ "/chart/2y?token=pk_789e324748c04083b632315395a71cde")
        
        
        if response:
            data = json.loads(response.text)
            x = []
            y = []
            
            for line in data[:1000]:
                not_closed = line["open"]#x column 1 -- this means open lol
                volume = line["volume"]#x column 2
                change = line["change"]#y
                
                inner_list = [not_closed, volume]

                
                x.append(inner_list)
                y.append(change>0)
                    
            print(x)
            print(y)
            
            #Load data into x and y lists
            #x is a 2D list
            
            if ml.lower() == "decision tree" or validation == "yes":
                
                #Build DT
                clf_dt = sklearn.tree.DecisionTreeClassifier()
                clf_dt = clf_dt.fit(x,y)
                
                if ml.lower() == "decision tree":

                     #Show visual of tree (flowchart)
                    sklearn.tree.plot_tree(clf_dt, feature_names = ["open", "volume", "marriage"], class_names = ["No Change", "Increase"])
                    plt.show()


                    #Predict win/loss for new data
                    new_values = [[not_closed_input, volume_input]]
                    if clf_dt.predict(new_values)[0]:
                        print("Price Increase")
                    else:
                        print("Price Decrease")
                    
                

          
            if ml.lower() == "knn" or validation == "yes":
                    
                #Build KNN
                    
                clf_knn = sklearn.neighbors.KNeighborsClassifier(5)
                clf_knn = clf_knn.fit(x,y)
                
                if ml.lower() == "knn":

                    #Predict win/loss for new data
                    new_values = [[not_closed_input, volume_input]]
                    if clf_knn.predict(new_values)[0]:
                        print("Price Increase")
                    else:
                        print("Price Decrease")
                
            if ml.lower() == "neural network" or validation == "yes":
                    
                #Build NN
                    
                clf_nn = sklearn.neural_network.MLPClassifier(solver = "lbfgs")
                clf_nn = clf_nn.fit(x,y)
                
                if ml.lower() == "neural network":
                
                    #Predict win/loss for new data
                    new_values = [[not_closed_input, volume_input]]
                    if clf_nn.predict(new_values)[0]:
                        print("Price Increase")
                    else:
                        print("Price Decrease")
                
            if validation == "yes":
                x_test = []
                y_test = []
                
                for line in data[1000:]:
                    not_closed_test = line["open"]#x column 1 -- this means open lol
                    volume_test = line["volume"]#x column 2
                    change_test = line["change"]#y
                    
                    inner_list_test = [not_closed_test, volume_test]

                    
                    x_test.append(inner_list_test)
                    y_test.append(change_test>0)
                    
              
                #Generate predictions for each machine learning model
                predicted_dt = clf_dt.predict(x_test)
                predicted_nn = clf_nn.predict(x_test)
                predicted_knn = clf_knn.predict(x_test)
                
                #Generate tables for each machine learning model
                print("Neural Network")
                print(sklearn.metrics.classification_report(y_test, predicted_nn, target_names = ["decrease", "increase"]))

                print("Decision Tree")
                print(sklearn.metrics.classification_report(y_test, predicted_dt, target_names = ["decrease", "increase"]))
                
                print("KNN")
                print(sklearn.metrics.classification_report(y_test, predicted_knn, target_names = ["decrease", "increase"]))

            if visualization == "yes":
                interested_objects = []
                
                correct_start_date = 0
                correct_end_date = 0
        
                for line in data:
                    if start_date:
                        correct_start_date = str(line["date"]) >= str(start_date)
                    if end_date:
                        correct_end_date = str(line["date"]) <= str(end_date)
                        
                    has_change = line["change"] is not None

                    if correct_start_date and correct_end_date and has_change:
                        # then this is an object we're interested in
                        interested_objects.append(line)
                    
                dates_list = []
                change_list = []
                for line in interested_objects:
                    dates_list.append(str(line["date"]))
                    change_list.append(line["change"])

                plt.title("Stock Price Change Over Time")
                plt.xlabel("Date")
                plt.ylabel("Change")
                plt.plot(dates_list,change_list)
                plt.xticks(rotation = 90, ha = "right") 

                plt.show()

            
            repeat = input("Would you like to predict another stock price?").lower()

            
            
            
        else:
            print("Sorry, could not connect.")
            
print("Thanks for using Brown Sugar's Stock Price Prediction Program!")


            
