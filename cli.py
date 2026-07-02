import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import print as rprint

from bot.orders import place_order
from bot.exceptions import TradingBotException
from bot.helpers import format_datetime

app = typer.Typer(help="Binance Futures Trading Bot CLI")
console = Console()

def print_banner():
    banner = Panel.fit(
        "[bold cyan]Binance Futures Trading Bot[/bold cyan]\n[blue]Binance Futures Testnet[/blue]",
        title="🤖",
        border_style="cyan"
    )
    console.print(banner)

@app.command()
def trade():
    """Interactive command to place a trade."""
    print_banner()
    
    symbol = typer.prompt("Symbol (e.g. BTCUSDT)")
    side = typer.prompt("Side (BUY/SELL)").upper()
    order_type = typer.prompt("Order Type (MARKET/LIMIT/STOP)").upper()
    quantity = typer.prompt("Quantity", type=float)
    
    price = None
    stop_price = None
    
    if order_type in ["LIMIT", "STOP"]:
        price = typer.prompt("Price", type=float)
        
    if order_type == "STOP":
        stop_price = typer.prompt("Stop Price", type=float)
        
    console.print("\n")
    summary = Table(show_header=False, box=None)
    summary.add_column("Key", style="bold cyan")
    summary.add_column("Value", style="yellow")
    summary.add_row("Symbol", symbol)
    summary.add_row("Side", side)
    summary.add_row("Order Type", order_type)
    summary.add_row("Quantity", str(quantity))
    if price:
        summary.add_row("Price", str(price))
    if stop_price:
        summary.add_row("Stop Price", str(stop_price))
        
    console.print(Panel(summary, title="[bold]Order Summary[/bold]", border_style="cyan"))
    
    confirm = typer.confirm("Place this order?")
    if not confirm:
        console.print("[red]Order cancelled by user.[/red]")
        raise typer.Exit()
        
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(description="Placing order...", total=None)
            response = place_order(
                symbol=symbol,
                side=side,
                order_type=order_type,
                quantity=quantity,
                price=price,
                stop_price=stop_price
            )
            
        success_table = Table(title="[bold green]Order Successfully Placed[/bold green]")
        success_table.add_column("Field", style="cyan")
        success_table.add_column("Value", style="green")
        
        success_table.add_row("Order ID", str(response.get("orderId", "N/A")))
        success_table.add_row("Status", str(response.get("status", "N/A")))
        success_table.add_row("Executed Qty", str(response.get("executedQty", "0")))
        success_table.add_row("Average Price", str(response.get("avgPrice", "0")))
        
        if "updateTime" in response:
            success_table.add_row("Timestamp", format_datetime(response["updateTime"]))
            
        console.print(success_table)
        
    except TradingBotException as e:
        console.print(Panel(f"[bold red]Error:[/bold red] {str(e)}", title="❌ Failed", border_style="red"))
    except Exception as e:
        console.print(Panel(f"[bold red]Unexpected Error:[/bold red] {str(e)}", title="❌ Failed", border_style="red"))

if __name__ == "__main__":
    app()
