import BetterRich
import sys
import os
from importlib import util
import argparse
from filecheck import Isfile
import time
from Keyword import load_keywords, check_success

#flags
parser = argparse.ArgumentParser(description="AI security check by file")
parser.add_argument("-t", "--target", required=True, help="Target AI file to check")
parser.add_argument("-f", "--function", required=True, help="The function in your file that provides the chat")
parser.add_argument("-p", "--payload", required=True, help="Payloads to test")
parser.add_argument("-d", "--debugmode", action='store_true', help="Enable debug mode to see full error details")
parser.add_argument("-s", "--success-keywords", help="File containing success keywords/phrases (one per line)")
parser.add_argument("-v", "--verbose", action='store_true', help="Show detailed output for each prompt (default: only show final summary)")
args = parser.parse_args()

#load target function
def load_target(targetfile, functionName):
    module_name = targetfile.replace(".py", "").replace("/", ".").replace("\\", ".")
    spec = util.spec_from_file_location(module_name, targetfile)
    module = util.module_from_spec(spec)
    spec.loader.exec_module(module)
    theFunc = getattr(module, functionName)
    return theFunc

#main
def spartan_rage(payload, func, debugmode, keywords, verbose):
    results = []
    try:
        if Isfile(payload) is True:
            with open(payload, "r", encoding="utf-8") as f:
                prompts = [line.strip() for line in f if line.strip()]
            
            for idx, prompt in enumerate(prompts, 1):
                try:
                    if verbose:
                        BetterRich.bold("---Senting prompt---")
                    
                    respond = func(prompt)
                    
                    if verbose:
                        BetterRich.good(f"Prompt sent: {prompt}")
                        BetterRich.good(f"---Getting respond---")
                    
                    time.sleep(1)
                    
                    if verbose:
                        print(respond)
                    
                    matched = check_success(respond, keywords)
                    if matched and verbose:
                        BetterRich.good(f"⚠️  SUCCESS - matched keyword: '{matched}'")
                    
                    results.append({"prompt": prompt, "response": respond, "success": bool(matched), "matched": matched})
                    
                    if verbose:
                        print()
                    time.sleep(0.3)
                
                except Exception as e:
                    if debugmode is True:
                        print(e)
                    else:
                        BetterRich.warn("An Error occured while running the program, to see the error, run the script in debug mode, e.g: python main.py -d ...")

        if Isfile(payload) is False:
            try:
                if verbose:
                    BetterRich.bold("---Senting prompt---")
                
                respond = func(payload)
                
                if verbose:
                    BetterRich.good(f"Prompt sent: {payload}")
                    BetterRich.good(f"---Getting respond---")
                    print(respond)
                    print()
                
                matched = check_success(respond, keywords)
                results.append({"prompt": payload, "response": respond, "success": bool(matched), "matched": matched})

            except Exception as e:
                if debugmode is True:
                    print(e)
                else:
                    BetterRich.warn("An Error occured while running the program, to see the error, run the script in debug mode, e.g: python main.py -d ...")

    except Exception as e:
        if debugmode is True:
            print(e)
        else:
            BetterRich.warn("An Error occured while running the program, to see the error, run the script in debug mode, e.g: python main.py -d ...")
    
    return results

def print_summary(results):
    if not results:
        return
    success_count = sum(r["success"] for r in results)
    BetterRich.bold(f"\n=== SUMMARY: {success_count}/{len(results)} payloads succeeded ===")
    for r in results:
        if r["success"]:
            BetterRich.warn(f"❌ VULNERABLE: \"{r['prompt'][:60]}...\" → matched '{r['matched']}'")

#clerifing function
try:
    theFunc = load_target(args.target, args.function)
except Exception as e:
    if args.debugmode is True:
        print(e)
    else:
        BetterRich.warn("An Error occured while running the program, to see the error, run the script in debug mode, e.g: python main.py -d ...")

if __name__ == "__main__":
    keywords = load_keywords(args.success_keywords)
    results = spartan_rage(args.payload, theFunc, args.debugmode, keywords, args.verbose)
    print_summary(results)
