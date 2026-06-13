
import os
import shutil

def mirror_to_json(source_path, mirror_directory="data_logs/mirror"):
   """
   Copies a JSON log file to the mirror directory.

   Parameters:
   - source_path (str): Path to the original JSON file to be mirrored.
   - mirror_directory (str): Destination folder for mirrored files.

   Returns:
   - dest_path (str): Path of the mirrored file, or None if source not found.
   """
   if not os.path.exists(source_path):
       print(f"⚠️ Source file not found: {source_path}")
       return None

   # Ensure the mirror directory exists
   os.makedirs(mirror_directory, exist_ok=True)

   # Extract the filename and build destination path
   filename = os.path.basename(source_path)
   dest_path = os.path.join(mirror_directory, filename)

   # Copy the file over
   shutil.copy2(source_path, dest_path)

   print(f"✅ Mirrored: {source_path} → {dest_path}")
   return dest_path

if __name__ == "__main__":
   # Quick test — mirrors cenos_data.json if it exists
   result = mirror_to_json("cenos_data.json")
   if result:
       print(f"💾 Mirror path: {result}")
