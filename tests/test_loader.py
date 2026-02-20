from src.data_loader import FinancialDataLoader

def test_tesla_data():
    loader = FinancialDataLoader("TSLA")
    data = loader.get_stock_history(period="5d")
    
    # Un test d'ingénieur : on vérifie que les données ne sont pas vides
    assert not data.empty
    print("Test réussi : Données Tesla récupérées avec succès !")

if __name__ == "__main__":
    test_tesla_data()