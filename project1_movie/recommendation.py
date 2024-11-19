import scipy
import pickle
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity
import constant_value as const
from post_method import get_recommendations

def contend_based_recommendations(movie, titles):
    """read matrix create similarity function and call main function"""
    tfidf_matrix = scipy.sparse.load_npz('tfidf_matrix.npz')
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    return get_recommendations(movie, titles, cosine_sim)