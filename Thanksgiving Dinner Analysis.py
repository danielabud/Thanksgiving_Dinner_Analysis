
# coding: utf-8

# In[1]:


import pandas as pd
data = pd.read_csv("thanksgiving.csv", encoding = "Latin-1")
print(data.head)


# In[2]:


data.columns


# In[3]:


#counts how many people celebrate thanksgiving
data["Do you celebrate Thanksgiving?"].value_counts()
#only counts people who DO celebrate thanksgiving
data = data[data["Do you celebrate Thanksgiving?"] == "Yes"]


# In[4]:


#defines the different options for main dish of people who celebrate thanksgiving
data["What is typically the main dish at your Thanksgiving dinner?"].value_counts()

tofurkey_only = data[data["What is typically the main dish at your Thanksgiving dinner?"] == "Tofurkey"]
print(tofurkey_only["Do you typically have gravy?"])


# In[5]:


#defines whether that particular pie was eaten (boolean). 
#ate_pies defines whether ANY type of pie was eaten
apple_isnull = pd.isnull(data["Which type of pie is typically served at your Thanksgiving dinner? Please select all that apply. - Apple"])
pumpkin_isnull = pd.isnull(data["Which type of pie is typically served at your Thanksgiving dinner? Please select all that apply. - Pumpkin"])
pecan_isnull = pd.isnull(data["Which type of pie is typically served at your Thanksgiving dinner? Please select all that apply. - Pecan"])
ate_pies = apple_isnull & pumpkin_isnull & pecan_isnull
ate_pies.value_counts()


# In[12]:


#this function simply parses a string, such as "40 - 55" into 
#an integer by 1) checking if it's blank, 2) replacing "55+" with 
#"55", and taking only the first "word" in the string.
def age_check(string):
    if pd.isnull(string) == True:
        return None
    fixed = string.replace('+', ' ')
    string_list = fixed.split(" ")
    age = int(string_list[0])
    return int(age)

data["int_age"] = data["Age"].apply(age_check)

data["int_age"].describe()

#note that this is a very poor estimate of the ages since it is very skewed
#away from the median age of a range, and choosing instead the first
#part of the range (55+ is skewed towards 55, 20-30 is "20" rather than "25")


# In[7]:


#converts income to an integer
def income_convert(string):
    if pd.isnull(string) == True:
        return None
    fixed = string.replace("$", '')
    fixed = fixed.replace(",", '')
    #rearrange these for higher computing efficiency if needed!
    string_list = fixed.split(" ")
    if string_list[0] == "Prefer":
        return None
    income = int(string_list[0])
    return income

#data[int_income] is now only integers or "none"
data["int_income"] = data["How much total combined money did all members of your HOUSEHOLD earn last year?"].apply(income_convert)
data["int_income"].describe()


# In[8]:


#selects only data where income is less than 150k from the "How far" column
#Then, it counts the results of each possible answer from "How far"

data[data["int_income"] < 150000]["How far will you travel for Thanksgiving?"].value_counts()
data[data["int_income"] > 150000]["How far will you travel for Thanksgiving?"].value_counts()


# In[14]:


#we are going to create a pivot table to analyze ages of "Yes"
#answers for each question

data.pivot_table(
    index="Have you ever tried to meet up with hometown friends on Thanksgiving night?", 
    columns='Have you ever attended a "Friendsgiving?"',
    values="int_income"
)

data.pivot_table(
    index = "Have you ever tried to meet up with hometown friends on Thanksgiving night?", 
    columns = "Have you ever attended a \"Friendsgiving?\"", 
    values= "int_age"
)

