from app.Services.SequenceProcessor import *


def make_prediction(models, sequence, selected_models):
    model_SVM, model_RF, model_NN = models

    sequences = [seq.strip() for seq in sequence.replace(",", " ").split() if seq.strip()]

    all_predictions = []  # Lista para acumular las predicciones de todas las secuencias

    for seq in sequences:
        probabilities = {}

        try:
            encoded_sequence = process_sequence(seq)

            if "SVM" in selected_models:
                probabilities["SVM_probability"] = round(model_SVM.predict_proba(encoded_sequence)[0][1], 2)
            else:
                probabilities["SVM_probability"] = None

            if "RF" in selected_models:
                probabilities["RandomForest_probability"] = round(model_RF.predict_proba(encoded_sequence)[0][1], 2)
            else:
                probabilities["RandomForest_probability"] = None

            if "NN" in selected_models:
                probabilities["NeuralNetwork_probability"] = round(model_NN.predict_proba(encoded_sequence)[0][1], 2)
            else:
                probabilities["NeuralNetwork_probability"] = None

            valid_probabilities = [
                value for value in probabilities.values()
                if value is not None and isinstance(value, (int, float))
            ]
            avg_probability = (
                round(sum(valid_probabilities) / len(valid_probabilities), 2)
                if valid_probabilities
                else None
            )

            probabilities["input_sequence"] = seq
            probabilities["average_probability"] = avg_probability
            probabilities["final_prediction"] = (
                "It's an Antimicrobial peptide"
                if avg_probability is not None and avg_probability >= 0.5
                else "It is not an Antimicrobial peptide"
            )

            # Aquí no se deben usar un array extra, simplemente agregar las predicciones
            all_predictions.append(probabilities)  # Sin el doble corchete []

        except Exception as e:
            all_predictions.append({
                "input_sequence": seq,
                "error": str(e)
            })

    return all_predictions if all_predictions else None
