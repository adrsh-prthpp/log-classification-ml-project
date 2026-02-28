from sentence_transformers import SentenceTransformer
import joblib

transformer_model = SentenceTransformer('all-MiniLM-L6-v2')
classifier_model = joblib.load('models/log_classifier.joblib')

def classify_with_bert(log_message):
    message_embedding = transformer_model.encode(log_message)
    probabilities = classifier_model.predict_proba([message_embedding])[0]
    if max(probabilities) < 0.5:
        return "Unclassified"
    predicted_label = classifier_model.predict([message_embedding])[0]

    return predicted_label


