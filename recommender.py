import pandas as pd
import re
import numpy as np
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import BM25

nltk.download('stopwords')
nltk.download('punkt')

class OutfitRecommender:

    def __init__(self, filename, columns, t_column, d_column, f_column, c_column, b_column):
        self.filename = filename
        self.columns = columns
        self.title_column = t_column
        self.description_column = d_column
        self.fabric_column = f_column  #  fabric column
        self.color_column = c_column  #  color column
        self.brand_column = b_column  #  brand column
        self.df = None

    def process(self, show=True):
        self.df = pd.read_csv(self.filename)
        self.df = self.df[self.columns]
        self.df[self.description_column].fillna('', inplace=True)
        self.df[self.description_column] = self.df[self.title_column] + '. ' +  self.df[self.description_column].map(str)
        self.df.dropna(inplace=True)
        self.df.drop_duplicates(inplace=True)
        return self.df

    def show_df_records(self, n = 5):
        return self.df.head(n)

    def show_info_details(self):
        return self.df.info()

    def __normalize(self, d):
        stopwords = nltk.corpus.stopwords.words('english')
        d = re.sub(r'[^a-zA-Z0-9\s]', '', d, re.I|re.A)
        d = d.lower().strip()
        tks = nltk.word_tokenize(d)
        f_tks = [t for t in tks if t not in stopwords]
        return ' '.join(f_tks)

    def get_normalized_corpus(self, tokens = False):
        n_corpus = np.vectorize(self.__normalize)        
        if tokens == True:
            norm_courpus = n_corpus(list(self.df[self.description_column]))
            return np.array([nltk.word_tokenize(d) for d in norm_corpus])            
        else:
            return n_corpus(list(self.df[self.description_column]))
    
    def search_outfits_by_brand(self, term='fabric'):
        category_column = self.fabric_column if term == 'fabric' else (
            self.color_column if term == 'fabric' else self.fabric_column
        )
        outfits = self.df[self.title_column].values
        possible_options = [
            (i, outfit)
            for i, outfit in enumerate(outfits)
            for word in outfit.split(' ')
            if word == category
        ]
        return possible_options

    def search_outfits_by_brand(self, term='color'):
        category_column = self.color_column if term == 'color' else (
            self.color_column if term == 'color' else self.color_column
        )
        outfits = self.df[self.title_column].values
        possible_options = [
            (i, outfit)
            for i, outfit in enumerate(outfits)
            for word in outfit.split(' ')
            if word == category
        ]
        return possible_options
    
    def search_outfits_by_brand(self, term='brand'):
        category_column = self.brand_column if term == 'branc' else (
            self.color_column if term == 'brand' else self.brand_column
        )
        outfits = self.df[self.title_column].values
        possible_options = [
            (i, outfit)
            for i, outfit in enumerate(outfits)
            for word in outfit.split(' ')
            if word == category
        ]
        return possible_options
            
    def get_features(self, norm_corpus):
        tf_idf = TfidfVectorizer(ngram_range=(1,2), min_df=2)
        tfidf_array = tf_idf.fit_transform(norm_corpus)
        return tfidf_array
    
    def get_vector_cosine(self, tfidf_array):
        return pd.DataFrame(cosine_similarity(tfidf_array))

    def get_bm25_weights(self, corpus):

        bm25 = BM25(corpus)
        avg_idf = sum(float(val) for val in bm25.idf.values()) / len(bm25.idf)

        weights = []
        for doc in corpus:
            scores = bm25.get_scores(doc, avg_idf)
            weights.append(scores)

        return pd.DataFrame(weights)
        
    def get_`bert`_weights(self, corpus):
        model = SentenceTransformer('bert-base-nli-mean-tokens')
        vectors = model.encode(corpus)
        weights = pd.DataFrame(cosine_similarity(vectors))
        
        return weights
    
    # search outfits based on fabric, color, brand
    def search_outfits_by_term(self, term='outfit'):
        outfits = self.df[self.title_column].values
        possible_options = [(i, outfit) for i, outfit in enumerate(outfits) for word in outfit.split(' ') if word == term]
        return possible_options
    
    # returns outfit recommendations for each product category
    def outfit_ recommendation(self, index, vector, n):
        similarities = vector.iloc[index].values
        similar_indices = np.argsort(-similarities)[1:n + 1]
        outfits = self.df[self.title_column].values
        similar_outfits =  outfits[similar_indices]
        return similar_outfits
