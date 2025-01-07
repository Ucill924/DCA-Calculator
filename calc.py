import csv
from colorama import Fore, Style, init
init(autoreset=True)
class DCACalculator:
    def __init__(self):
        self.investments = []
    def add_purchase(self, price, tokens):
        """Menambahkan data pembelian ke dalam list."""
        self.investments.append({'price': price, 'tokens': tokens})
    def calculate_dca(self):
        """Menghitung harga rata-rata (DCA) dan total token."""
        total_cost = sum(item['price'] * item['tokens'] for item in self.investments)
        total_tokens = sum(item['tokens'] for item in self.investments)
        average_price = total_cost / total_tokens if total_tokens > 0 else 0
        return average_price, total_tokens
    def calculate_profit_loss(self, current_price):
        """Menghitung total keuntungan atau kerugian berdasarkan harga pasar saat ini."""
        total_tokens = sum(item['tokens'] for item in self.investments)
        total_cost = sum(item['price'] * item['tokens'] for item in self.investments)
        current_value = current_price * total_tokens
        profit_loss = current_value - total_cost
        return profit_loss, current_value
def load_purchases_from_csv(file_path):
    purchases = []
    current_price = 0
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header
        for row in reader:
            if row[0] == "current_price":
                current_price = float(row[1])
            else:
                price = float(row[0])
                tokens = float(row[1])
                purchases.append({'price': price, 'tokens': tokens})
    return purchases, current_price
if __name__ == "__main__":
    dca_bot = DCACalculator()
    purchases, current_price = load_purchases_from_csv("purchases.csv")
    for purchase in purchases:
        dca_bot.add_purchase(purchase['price'], purchase['tokens'])

    # Menghitung rata-rata harga beli (DCA)
    average_price, total_tokens = dca_bot.calculate_dca()
    print(f"Rata-rata harga beli (DCA): ${average_price:.2f}")
    print(f"Total token: {total_tokens:.2f}")
    profit_loss, current_value = dca_bot.calculate_profit_loss(current_price)
    usd_to_idr = 16000
    total_value_idr = current_value * usd_to_idr
    profit_loss_idr = profit_loss * usd_to_idr
    if profit_loss > 0:
        profit_loss_text = f"{Fore.GREEN}${profit_loss:.2f} ({profit_loss_idr:,.2f} IDR)"
    else:
        profit_loss_text = f"{Fore.RED}${profit_loss:.2f} ({profit_loss_idr:,.2f} IDR)"
    print(f"Total keuntungan/kerugian pada harga ${current_price}: {profit_loss_text}")
    print(f"Total nilai USD pada harga saat ini: ${current_value:.2f} ({total_value_idr:,.2f} IDR)")
