"""
Test unitaire pour hello.py
"""
import hello

def test_hello():
    """Teste que la fonction hello() retourne le message attendu."""
    assert hello.hello() == "Hello, le workbench!"