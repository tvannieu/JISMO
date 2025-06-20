#!/usr/bin/env python3
import shutil
from pathlib import Path

def encode_vfrac(val):
    return f"{int(float(val) * 100):02d}"

def encode_del0(val):
    return 'pdg' if val == 'pdg' else f"d{int(float(val)):02d}"

def prompt_with_default(prompt, default):
    val = input(f"{prompt} [{default}]: ").strip()
    return val if val else default

def main():
    import sys
    if len(sys.argv) != 2:
        print("Usage: ./copy_qfiles.py <target_model_folder>")
        sys.exit(1)

    model_path = Path(sys.argv[1]).resolve()
    input_dir = model_path / "Input"
    qfile_dir = Path(__file__).resolve().parents[1] / "Qfile"

    # Prompt user input
    por = prompt_with_default("Porosity", "0.00")
    vvac = prompt_with_default("Vacuum fraction", "0.05")
    ab = prompt_with_default("Axis ratio a/b", "1.5")
    del0 = prompt_with_default("del0", "00.2")

    por_code = encode_vfrac(por)
    vvac_code = encode_vfrac(vvac)
    ab_str = ab
    del0_code = encode_del0(del0)

    input_dir.mkdir(parents=True, exist_ok=True)

    # Map of types to desired destination filenames
    files = {
        "Dark": f"d.Dk{vvac_code}ab{ab_str}{del0_code}",
        "aC":   f"d.aC{por_code}ab{ab_str}{del0_code}",
        "Si":   f"d.Si{por_code}ab{ab_str}{del0_code}",
    }

    for typ, fname in files.items():
        source = qfile_dir / fname
        target_name = f"d.Qellip{typ}"
        target = input_dir / target_name        
        if not source.exists():
            print(f"ERROR: File not found: {source}")
        else:
            shutil.copy(source, target)
            base_dir = Path(__file__).resolve().parent.parent
            print(f"Copied: {source.name} → {target.relative_to(base_dir / 'models')}")

if __name__ == "__main__":
    main()