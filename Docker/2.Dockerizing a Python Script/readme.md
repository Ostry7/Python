# Python Data Processing in Docker

This project demonstrates how to run a simple **Python data processing script** inside a Docker container.  
The script loads a CSV file using **pandas** and prints basic statistics to the console.

## Files

- `Dockerfile` – defines how to build the container image  
- `process_data.py` – Python script that reads and analyzes a CSV file  
- `requirements.txt` – Python dependencies (`pandas`)  
- `people-10000.csv` – example dataset to process  

## How to run

1. **Build the image:**
   ```bash
   docker build -t data-processor .
   ```

2. **Run the container with local CSV file mounted:**
   ```bash
   docker run -v "C:\PATH:/app" data-processor
   ```

   > 💡 Make sure that `people-10000.csv` is located in the same directory as `process_data.py`.

3. **View the output:**
   The terminal will display statistical summary of the dataset (from `pandas.DataFrame.describe()`).

## Example output

```
         age       height       weight
count  10000  10000.00000  10000.00000
mean      35     170.123      71.456
std       12       10.458      14.982
min       18      145.0        45.0
max       75      200.0       110.0
```

