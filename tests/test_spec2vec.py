import os
import gensim
import numpy
import pytest
from matchms import Spectrum
from spec2vec import Spec2Vec
from spec2vec import SpectrumDocument


def test_spec2vec_pair_method():
    """Test if pair of two SpectrumDocuments is handled correctly"""
    spectrum_1 = Spectrum(mz=numpy.array([100, 150, 200.]),
                          intensities=numpy.array([0.7, 0.2, 0.1]),
                          metadata={'id': 'spectrum1'})
    spectrum_2 = Spectrum(mz=numpy.array([100, 140, 190.]),
                          intensities=numpy.array([0.4, 0.2, 0.1]),
                          metadata={'id': 'spectrum2'})

    documents = [SpectrumDocument(s) for s in [spectrum_1, spectrum_2]]
    model = load_test_model()
    spec2vec = Spec2Vec(model=model, intensity_weighting_power=0.5)
    score01 = spec2vec.pair(documents[0], documents[1])
    assert score01 == pytest.approx(0.9936808, 1e-6)
    score11 = spec2vec.pair(documents[1], documents[1])
    assert score11 == pytest.approx(1.0, 1e-9)


def test_spec2vec_matrix_method():
    """Test if matrix of 2x2 SpectrumDocuments is handled correctly"""
    spectrum_1 = Spectrum(mz=numpy.array([100, 150, 200.]),
                          intensities=numpy.array([0.7, 0.2, 0.1]),
                          metadata={'id': 'spectrum1'})
    spectrum_2 = Spectrum(mz=numpy.array([100, 140, 190.]),
                          intensities=numpy.array([0.4, 0.2, 0.1]),
                          metadata={'id': 'spectrum2'})

    documents = [SpectrumDocument(s) for s in [spectrum_1, spectrum_2]]
    model = load_test_model()
    spec2vec = Spec2Vec(model=model, intensity_weighting_power=0.5)
    scores = spec2vec.matrix(documents, documents)
    assert scores[0, 0] == pytest.approx(1.0, 1e-9), "Expected different score."
    assert scores[1, 1] == pytest.approx(1.0, 1e-9), "Expected different score."
    assert scores[1, 0] == pytest.approx(0.9936808, 1e-6), "Expected different score."
    assert scores[0, 1] == pytest.approx(0.9936808, 1e-6), "Expected different score."


def load_test_model():
    """Load pretrained Word2Vec model."""
    repository_root = os.path.join(os.path.dirname(__file__), "..")
    model_file = os.path.join(repository_root, "integration-tests", "test_user_workflow_spec2vec.model")
    assert os.path.isfile(model_file), "Expected file not found."
    return gensim.models.Word2Vec.load(model_file)