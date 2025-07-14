import multiprocessing
from backend.crew.crew_runner import run_growth_agent_if_same_domain

def run_in_subprocess(ch1_data, ch2_data):
    manager = multiprocessing.Manager()
    return_dict = manager.dict()

    def run(return_dict):
        try:
            result = run_growth_agent_if_same_domain(ch1_data, ch2_data)
            return_dict["result"] = result
        except Exception as e:
            return_dict["error"] = str(e)

    p = multiprocessing.Process(target=run, args=(return_dict,))
    p.start()
    p.join(timeout=60)

    if "error" in return_dict:
        raise RuntimeError(return_dict["error"])
    return return_dict.get("result", None)
