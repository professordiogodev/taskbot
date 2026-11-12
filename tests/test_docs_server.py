import docs_server as d

def test_tokenize_remove_acentos_e_stopwords():
    assert d.tokenize("Decisões de ficheiro") == ["decisoes", "ficheiro"]

def test_search_sem_resultado():
    assert d.search_docs("receita de bolo xyzzy") == "Nada relevante encontrado."