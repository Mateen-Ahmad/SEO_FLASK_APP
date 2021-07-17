from flask import Flask, render_template, request
from tensorflow.keras.models import load_model
import copy, requests



app = Flask(__name__)
# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


@app.route('/')
def index():
    return render_template('homepage.html')


@app.route('/check')
def check():
    # a = 1
    data = requests.get('https://seoapi.herokuapp.com/shoes/https://www.bata.com.pk/')
    data = data.json()

    return data
@app.route('/services', methods=['POST', 'GET'])
def nev_services():
    return render_template('services.html')


@app.route('/contact')
def nev_contact():
    return render_template('contact.html')

@app.route('/results', methods=['POST', 'GET'])
def nev_results():
    if request.method == 'POST':
        myurl = request.form['URL']
        keyword = request.form['keyword']
        data = requests.get('https://seoapi.herokuapp.com/'+ keyword +'/' + myurl)
        data = data.json()

        return render_template('results.html', myurl = myurl, keyword = keyword, data = data)
    else:
        return render_template('results.html')
    


@app.route('/suggestions', methods=['POST', 'GET'])
def suggestions():
    temp=''
    myurl=""
    keyword=""
    if request.method == 'POST':

        myurl = request.form['URL']
        keyword = request.form['keyword']
        data = requests.get('https://seoapi.herokuapp.com/'+ keyword +'/' + myurl)
        temp = data.json()
        filtered = copy.deepcopy(temp)
        delete = ['Keyword', 'Rank', 'Title_Of_Page', 'URL', 'Domain_Name']
        for i in delete:
            del filtered[i]
        
        abc = [[]]
        for i in filtered.values():
            abc[0].append(i[0])
        print("abc", abc)

        

        model = load_model('ANN Model - 3 Classes.h5')
        y_pred = model.predict(abc)
        print (y_pred[0])
        y_pred_class = np.argmax(y_pred,axis=1)
        print(y_pred_class)

        temp['Rank'] = y_pred_class
        if temp['Lenght_Of_Title'][0] < 50 or temp['Lenght_Of_Title'][0] > 60:
            temp['Lenght_Of_Title'] = ['Length of Title shoud be between 50 to 60']
            temp['Lenght_Of_Title'].append(1)

        if temp['Lenght_of_Url'][0] > 60:
            temp['Lenght_of_Url'] = ['Length of Title shoud be less than 60']
            temp['Lenght_of_Url'].append(1)


        if temp['Presence_of_Keyword_in_Title'][0] == 0:
            temp['Presence_of_Keyword_in_Title'] = ['Please add keyword in your title']
            temp['Presence_of_Keyword_in_Title'].append(1)

        if temp['Title_Starts_with_Keyword'][0] == 0:
            temp['Title_Starts_with_Keyword'] = ['Please start your page title with keyword']
            temp['Title_Starts_with_Keyword'].append(1)

        if temp['Presence_Of_Keyword_In_Url'][0] == 0:
            temp['Presence_Of_Keyword_In_Url'] = ['Keyword should pe present in URL']
            temp['Presence_Of_Keyword_In_Url'].append(1)



        if temp['Presence_of_Keyword_in_H1_Tag'][0] == 0:
            temp['Presence_of_Keyword_in_H1_Tag'] = ['Keyword should be present in H1 Tag']
            temp['Presence_of_Keyword_in_H1_Tag'].append(1)
        if temp['Presence_of_Keyword_in_H2_Tag'][0] == 0:
            temp['Presence_of_Keyword_in_H2_Tag'] = ['Keyword should be present in H2 Tag']
            temp['Presence_of_Keyword_in_H2_Tag'].append(1)
        if temp['Presence_of_Keyword_in_H3_Tag'][0] == 0:
            temp['Presence_of_Keyword_in_H3_Tag'] = ['Keyword should be present in H3 Tag']
            temp['Presence_of_Keyword_in_H3_Tag'].append(1)

        if temp['Content_Lenght'][0] < 2000:
            temp['Content_Lenght'] = ['Content Lenght should be at least 2000']
            temp['Content_Lenght'].append(1)

        if temp['Keyword_Denisty'][0] < 1 or temp['Keyword_Denisty'][0] > 2:
            temp['Keyword_Denisty'] = ['Keyword Denisty should be around 1-2%']
            temp['Keyword_Denisty'].append(1)

        if temp['Keyword_in_Description'][0] == 0:
            temp['Keyword_in_Description'] = ['Keyword should be present in Description']
            temp['Keyword_in_Description'].append(1)
        if temp['Keyword_in_Alt_Tags_of_Images'][0] == 0:
            temp['Keyword_in_Alt_Tags_of_Images'] = ['Keyword should be present in Alt Tags of Images']
            temp['Keyword_in_Alt_Tags_of_Images'].append(1)

        if temp['Presence_of_Internal_Links'][0] == 0:
            temp['Presence_of_Internal_Links'] = ['Internal Links should be present to incease rank ']
            temp['Presence_of_Internal_Links'].append(1)
        if temp['Presence_of_External_Links'][0] == 0:
            temp['Presence_of_External_Links'] = ['External Links should be present to incease rank ']
            temp['Presence_of_External_Links'].append(1)
        # session['suggestions'] = temp
        return render_template('suggestions.html', data = temp, myurl = myurl, keyword = keyword)

    else:
        return render_template('suggestions.html', data = temp, myurl = myurl, keyword = keyword)



if __name__ == "__main__":
    app.run(debug=True)