import subprocess
import sys
import signal

# Function to run a script
def run_script(script_name):
    try:
        subprocess.run([sys.executable, script_name], check=True)
    except subprocess.CalledProcessError as e:
        print(f'Error running {script_name}: {e}')

# Main function to run both scripts
if __name__ == '__main__':
    processes = []
    try:
        # Starting SQL_query.py and Update_DB.py as concurrent processes
        p1 = subprocess.Popen([sys.executable, 'SQL_query.py'])
        p2 = subprocess.Popen([sys.executable, 'Update_DB.py'])
        processes.append(p1)
        processes.append(p2)

        # Wait for both processes to complete
        for p in processes:
            p.wait()
    except KeyboardInterrupt:
        print('Caught keyboard interrupt. Shutting down...')
    finally:
        # Gracefully terminating processes if they're still running
        for p in processes:
            if p.poll() is None:  # Process still running
                p.terminate()
                p.wait()  # Ensure the process has exited
        print('All processes have been terminated.'),
