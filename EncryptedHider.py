import os
import sys
import glob
from cryptography.fernet import Fernet

# Generate or load encryption key (you can use a fixed key or generate it dynamically)
# Use a static key if you need to use the same key for both split and reconstruct phases.
def load_key():
    """Loads the encryption key from a file or generates a new one."""
    key_path = "encryption_key.key"
    if not os.path.exists(key_path):
        key = Fernet.generate_key()
        with open(key_path, 'wb') as key_file:
            key_file.write(key)
    else:
        with open(key_path, 'rb') as key_file:
            key = key_file.read()
    return key

# Encryption function
def encrypt_data(data, fernet):
    return fernet.encrypt(data)

# Decryption function
def decrypt_data(data, fernet):
    return fernet.decrypt(data)

def split_video(video_path, chunk_size=1024):
    """Splits a video file into smaller encrypted text files."""
    try:
        # Load the encryption key and initialize Fernet
        key = load_key()
        fernet = Fernet(key)

        with open(video_path, 'rb') as f:
            data = f.read()
        
        # Split data into chunks
        chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]
        
        # Write encrypted chunks to separate text files
        for idx, chunk in enumerate(chunks):
            encrypted_chunk = encrypt_data(chunk, fernet)
            with open(f'chunk_{idx}.txt', 'wb') as chunk_file:
                chunk_file.write(encrypted_chunk)
        
        print(f"Video '{video_path}' split into {len(chunks)} encrypted chunks.")
        
        # Optionally delete the original video file
        os.remove(video_path)
        print(f"Original video file '{video_path}' deleted.")
    except Exception as e:
        print(f"Error splitting video: {e}")

def reconstruct_video(output_path):
    """Reconstructs the video file from the encrypted text file chunks."""
    try:
        # Load the encryption key and initialize Fernet
        key = load_key()
        fernet = Fernet(key)

        chunks = []
        # Filter and read only the chunk files
        for file in sorted(os.listdir('.'), key=lambda x: int(x.split('_')[1].split('.')[0]) if x.startswith('chunk_') else float('inf')):
            if file.endswith('.txt'):
                with open(file, 'rb') as chunk_file:
                    encrypted_chunk = chunk_file.read()
                    decrypted_chunk = decrypt_data(encrypted_chunk, fernet)
                    chunks.append(decrypted_chunk)
        
        # Write combined decrypted data to a new video file
        with open(output_path, 'wb') as video_file:
            video_file.write(b''.join(chunks))
        
        print(f"Reconstructed video saved as '{output_path}'.")
        
        # Optionally delete the chunk files after reconstruction
        for file in sorted(os.listdir('.'), key=lambda x: int(x.split('_')[1].split('.')[0]) if x.startswith('chunk_') else float('inf')):
            if file.endswith('.txt'):
                os.remove(file)
                print(f"Deleted chunk file '{file}'.")
    except Exception as e:
        print(f"Error reconstructing video: {e}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python Script_hider.py <command>")
        return

    command = sys.argv[1]

    if command == 'Go':
        # Check for .mp4 file in the current directory
        mp4_files = glob.glob("*.mp4")
        if mp4_files:
            split_video(mp4_files[0])  # Use the first .mp4 file found
        else:
            print("No .mp4 file found in the current directory.")
    elif command == 'Goed':
        # Reconstruct the video
        reconstruct_video("reconstructed_video.mp4")
    else:
        print("Invalid command. Use 'Go' to split or 'Goed' to reconstruct.")

if __name__ == "__main__":
    main()


