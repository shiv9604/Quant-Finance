help:           
	@echo "Commands:"                                                                             
	@echo "  make dev         — Test execution anytime (no time restrictions)"
	@echo "  make testnet     — UAT: real-world timing on testnet server"
	@echo "  make live        — Production: real account, real timing"                            
	@echo "  make dry         — Testnet, log only (no real orders)"
	@echo "  make replay      — Run replay against historical data"                               
				
dev: clean-state                                                                                    
	APP_ENV=dev python -m src.main
																									
testnet: clean-state
	APP_ENV=testnet python -m src.main                                                            
				
live: clean-state
	APP_ENV=live python -m src.main

dry: clean-state
	APP_ENV=testnet DRY_RUN=true python -m src.main
																									
replay:
	python -m src.replay.replay_runner                                                            
				
clean-state:
	@rm -f logs/state.json
	@echo "State cleared."