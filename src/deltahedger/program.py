import scalper, asyncio

def main():
	obj = scalper.Scalper("config.ini", "Deribit")
	asyncio.run(obj.run_loop())

if __name__ == "__main__":
    main()
