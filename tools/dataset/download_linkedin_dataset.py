import os
import urllib.request

def download_file(url, dest_path):
    print(f"Downloading {url} to {dest_path}...")
    try:
        def reporthook(block_num, block_size, total_size):
            read_so_far = block_num * block_size
            if total_size > 0:
                percent = (read_so_far * 100) / total_size
                print(f"\rProgress: {percent:.1f}% ({read_so_far}/{total_size} bytes)", end="")
            else:
                print(f"\rDownloaded {read_so_far} bytes", end="")
        urllib.request.urlretrieve(url, dest_path, reporthook)
        print("\nDownload complete!")
    except Exception as e:
        print(f"\nError: {e}")
        raise

def main():
    dest_dir = r"d:\PROJECTS\Internship-recommendation-engine\ai-service\dataset\original"
    os.makedirs(dest_dir, exist_ok=True)
    
    base_url = "https://raw.githubusercontent.com/prajaktawaghmare13/industry-skill-insights/main/data"
    
    download_file(f"{base_url}/job_postings.csv", os.path.join(dest_dir, "job_postings.csv"))
    download_file(f"{base_url}/job_skills.csv", os.path.join(dest_dir, "job_skills.csv"))
    download_file(f"{base_url}/job_summary.csv", os.path.join(dest_dir, "job_summary.csv"))
    print("LinkedIn job postings dataset files downloaded successfully!")

if __name__ == "__main__":
    main()
