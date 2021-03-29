from django.shortcuts import render
import pickle
import pathlib
import re
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from textblob import TextBlob
import textblob as tb
tb.en.spelling.update({'wow':1})

# Create your views here.
def restaurant_reviews_logistic(request):
    context = {
        'review': None,
        'color': None,
        'display': 'none',
    }

    if request.method =='POST':

        new_review = str(request.POST['review'])

        current_dir_path = pathlib.Path(__file__).parent.absolute()
        files_path = current_dir_path/'static'/'restaurant_reviews_logistic'
        model_filename = files_path/'logistic_regression_finalized_model.sav'
        sc_filename = files_path/'sc.sav'
        cv_filename = files_path/'cv.sav'
        classifier = pickle.load(open(model_filename, 'rb'))
        sc = pickle.load(open(sc_filename, 'rb'))
        cv = pickle.load(open(cv_filename, 'rb'))

        new_review = re.sub('[^a-zA-Z]', ' ', new_review)
        new_review = new_review.lower()
        new_review = new_review.split()
        ps = PorterStemmer()
        all_stopwords = stopwords.words('english')
        all_stopwords.remove('not')
        new_review = [ps.stem(word) for word in new_review if not word in set(all_stopwords)]
        new_review = ' '.join(new_review)
        new_review = str(TextBlob(new_review).correct())
        new_corpus = [new_review]
        new_X_test = cv.transform(new_corpus).toarray()
        new_X_test = sc.transform(new_X_test)
        new_y_pred = classifier.predict(new_X_test)
        if new_y_pred[0] == 1:
            context = {
                'review': 'Positive',
                'color': '#11998e',
                'display': 'block',
            }
            print('Positive')
        else:
            context = {
                'review': 'Negative',
                'color': 'red',
                'display': 'block',
            }
            print('Negative')

    return render(request, 'restaurant_reviews_logistic.html', context)
