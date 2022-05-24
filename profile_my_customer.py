import pandas as pd
from sklearn.naive_bayes import MultinomialNB



def linebreak():
    print("\n")



# Enconde the diet into an array of 0 and 1
def diet_encoder():
    while True:
        diet = input('Are you vegan or vegetarian?[yes/no] ').lower()
        if diet == 'yes':
            while True:
                spec = input('Could you please specify which? ').lower()
                if spec == 'vegan':
                    omnivorous = 0
                    vegetarian = 0
                    vegan = 1 
                    break
                elif spec == 'vegetarian':
                    omnivorous = 0
                    vegetarian = 1
                    vegan = 0
                    break
                else:
                    print("Sorry, I couldn't understand what you said, could you please type it again? ")
            break
        elif diet == 'no':
            omnivorous = 1
            vegetarian = 0
            vegan = 0
            break
        else:
            print("Sorry, I couldn't understand what you said, could you please type it again? ")
    diet_list = []
    diet_list.extend([omnivorous, vegetarian, vegan])
    
    return diet_list



# Returns an array with all the info for the model to predict    
def customer_input():

    age = input('Please input your age: ')
    income = input('What is your annual income? (in EUR) ')
    earnings = input('How much do you earn on average selling second hand stuff every month? (in EUR) ')
    diet_list = diet_encoder()
    diet_list

    # Motivations sell multiple choice
    motiv_list_sell = []
    list_options = [ 'a', 'b', 'c', 'd', 'e', 'f']
    motivations = input("\n\nSELLING BEHAVIOUR\nWhen selling second hand products, which one of the following situations describes you the best? (you can choose more than one) \n  A) When selling 2nd hand stuff, I want to get some money back of what that item cost me. \n  B) When selling 2nd hand stuff, I want to make money. \n  C) I sell 2nd hand stuff because I'm concerned with the environment and circular economy. \n  D) I prefer to donate my stuff rather than selling it \n  E) I'm lazy to post my stuff on 2nd hand apps/websites. \n  F) I have never considered selling 2nd hand stuff.\n\n" ).lower()
    
    for elem in list_options:
        if elem in motivations:
            motiv_list_sell.append(1)
        else:
            motiv_list_sell.append(0)


    # Categories to sell multiple choice
    cat_list_sell = []
    list_options = [ 'a', 'b', 'c', 'd', 'e', 'f', 'g']
    categories = input("\n\nSELLING CATEGORIES\nWhich are the categories that you usually sell on second hand apps? (you can choose more than one, type 'n' if you have never sold second hand products) \n  A) Clothes \n  B) Electronics \n  C) Collectibles \n  D) Books, CD, DVD's \n  E) Home & Garden \n  F) Sports & Leisure \n  G) Others \n\n" ).lower()
    
    for elem in list_options:
        if elem in categories:
            cat_list_sell.append(1)
        else:
            cat_list_sell.append(0)


    # Motivations buy multiple choice
    motiv_list_buy = []
    list_options = [ 'a', 'b', 'c', 'd', 'e', 'f']
    motivations = input("\n\nBUYING BEHAVIOUR\nWhen buying second hand products, which one of the following situations describes you the best? (you can choose more than one) \n  A) I buy 2nd hand stuff because Is cheaper than buying it first hand. \n  B) I only buy 2nd hand stuff for very specifical products. \n  C) I buy 2nd hand stuff because I wanna contribute with the environment and the circular economy. \n  D) When I want to buy something, checking on 2nd hand apps/websites is never my first option. \n  E) I don't like to buy used clothes or stuff. \n  F) I never considered the option of buying 2nd hand.\n\n" ).lower()
    
    for elem in list_options:
        if elem in motivations:
            motiv_list_buy.append(1)
        else:
            motiv_list_buy.append(0)


    # Categories to buy multiple choice
    cat_list_buy = []
    list_options = [ 'a', 'b', 'c', 'd', 'e', 'f', 'g']
    categories = input("\n\nBUYING CATEGORIES\nWhich are the categories that you usually buy on second hand apps? (you can choose more than one, type 'n' if you have never sold second hand products) \n  A) Clothes \n  B) Electronics \n  C) Collectibles \n  D) Books, CD, DVD's \n  E) Home & Garden \n  F) Sports & Leisure \n  G) Others \n\n" ).lower()
    
    for elem in list_options:
        if elem in categories:
            cat_list_buy.append(1)
        else:
            cat_list_buy.append(0)


    sell_array = []
    sell_array.extend([int(age),int(income),int(earnings)])
    sell_array = sell_array + diet_list + motiv_list_sell

    buy_array = []
    buy_array.extend([int(age),int(income)])
    buy_array = buy_array + diet_list + motiv_list_buy + cat_list_buy

    cat_array = []
    cat_array.extend([int(age),int(income)])
    cat_array = cat_array + diet_list + cat_list_sell + cat_list_buy
    
    return sell_array, buy_array, cat_array



# trains the model and returns a prediction for the input of the customer
def predict_model(array):
    secondhand = pd.read_excel('datasets/Merged_full_data_dummies.xlsx')


    # selling frequency
    column_array = ['age', 'annual_income', 'selling_earnings', 'omnivorous', 'vegetarian', 'vegan', 'sm_a_en', 'sm_b_en', 'sm_c_en', 'sm_d_en', 'sm_e_en', 'sm_f_en']
    X_train = secondhand.loc[:, column_array]
    y_train = secondhand['frequency_category']

    model = MultinomialNB()

    model.fit(X_train, y_train)
    
    prediction_sell = model.predict(pd.DataFrame(array[0], index=column_array).T)


    # buying frequency
    column_array = ['age', 'annual_income', 'omnivorous', 'vegetarian', 'vegan', 'bm_a_en', 'bm_b_en', 'bm_c_en', 'bm_d_en', 'bm_e_en', 'bm_f_en', 'bc_a_en', 'bc_b_en', 'bc_c_en', 'bc_d_en', 'bc_e_en', 'bc_f_en', 'bc_g_en']
    X_train = secondhand.loc[:, column_array]
    y_train = secondhand['buyer_category']

    model = MultinomialNB()

    model.fit(X_train, y_train)

    prediction_buy = model.predict(pd.DataFrame(array[1], index=column_array).T)


    # likely to use the platform 
    column_array = ['age', 'annual_income', 'omnivorous', 'vegetarian', 'vegan', 'sc_a_en', 'sc_b_en', 'sc_c_en', 'sc_d_en', 'sc_e_en', 'sc_f_en', 'sc_g_en', 'bc_a_en', 'bc_b_en', 'bc_c_en', 'bc_d_en', 'bc_e_en', 'bc_f_en', 'bc_g_en']
    X_train = secondhand.loc[:, column_array]
    y_train = secondhand['vinted']

    model = MultinomialNB()

    model.fit(X_train, y_train)
    
    prediction_platform = model.predict(pd.DataFrame(array[2], index=column_array).T)
    
    return prediction_sell[0], prediction_buy[0], prediction_platform[0]



# Translates the prediction of sell freq into a string
def translate_prediction_sell(element):
    if element == 1:
        return "-------------------------------------------------------------------------------------------------------\nNEVER SELLER:\nCustomer will be likely to never sell items on 2nd hand platforms.\n-------------------------------------------------------------------------------------------------------"
    elif element == 2:
        return "-------------------------------------------------------------------------------------------------------\nRARE SELLER:\nCustomer will be likely to rarely sell items on 2nd hand platforms, 2 listings or less every 3 months.\n-------------------------------------------------------------------------------------------------------"
    elif element == 3:
        return "-------------------------------------------------------------------------------------------------------\nOCCASIONAL SELLER:\nCustomer will be likely to occasionally sell items on 2nd hand platforms, 1 or 2 listings every month.\n-------------------------------------------------------------------------------------------------------"
    elif element == 4:
        return "-------------------------------------------------------------------------------------------------------\nOFTEN SELLER:\nCustomer will be likely to often sell items on 2nd hand platforms, 3 or 4 listings per month.\n-------------------------------------------------------------------------------------------------------"
    elif element == 5:
        return "-------------------------------------------------------------------------------------------------------\nREGULAR SELLER:\nCustomer will be likely to regularly sell items on 2nd hand platforms, 5 or more listings per month.\n-------------------------------------------------------------------------------------------------------"
    else:
        return "error"


# Translates the prediction of sell freq into a string
def translate_prediction_buy(element):
    if element == 1:
        return "-------------------------------------------------------------------------------------------------------\nLOW PROFILE BUYER:\nCustomer will be likely to spend less than 25EUR monthly buying second hand products.\n-------------------------------------------------------------------------------------------------------"
    elif element == 2:
        return "-------------------------------------------------------------------------------------------------------\nMEDIUM PROFILE BUYER:\nCustomer will be likely to spend between 25EUR and 50EUR monthly buying second hand products.\n-------------------------------------------------------------------------------------------------------"
    elif element == 3:
        return "-------------------------------------------------------------------------------------------------------\nHIGH PROFILE BUYER:\nCustomer will be likely to spend more than 50EUR monthly buying second hand products.\n-------------------------------------------------------------------------------------------------------"
    else:
        return "error"


# Translates the prediction of using the app
def translate_prediction_platform(element):
    if element == 1:
        return "-------------------------------------------------------------------------------------------------------\nPOTENTIAL VINTED USER:\nBased on the category of the items that the customer buys and sells, the customer is a potential\nuser of the Vinted app.\n-------------------------------------------------------------------------------------------------------\n-------------------------------------------------------------------------------------------------------\n\n"
    elif element == 0:
        return "-------------------------------------------------------------------------------------------------------\nNON-POTENTIAL VINTED USER:\nBased on the category of the items that the customer buys and sells, the customer is NOT a potential\nuser of the Vinted app.\n-------------------------------------------------------------------------------------------------------\n-------------------------------------------------------------------------------------------------------\n\n"
    else:
        return "error"



# Main funtcion for the seller prediction
def main_sell():
    linebreak()
    print("Hello, welcome to ProfileMyCustomer(TM)!\n\nYou are logged in as Vinted UAB (guest);\nuserId:345566545461\n\n\nINPUT YOUR DATA IN ORDER TO EARN A 25% DISCOUNT\nON YOUR NEXT PURCHASE ON THE VINTED APP!! ")
    linebreak()

    input_info = customer_input()
    input_info

    prediction = predict_model(input_info)
    prediction

    output1 = translate_prediction_sell(prediction[0])
    output1

    output2 = translate_prediction_buy(prediction[1])
    output2

    output3 = translate_prediction_platform(prediction[2])
    output3
    print("\n-------------------------------------------CUSTOMER INSIGHTS-------------------------------------------")
    print(output1)
    print(output2)
    print(output3)


main_sell()