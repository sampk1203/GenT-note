# **GenT-Note**  

**GenT-Note** is a tool designed to:   
- Generate a **note sequence** from a provided TPM.  

### **File Format**  
Sample TPM files are provided with the `.tpm` extension.  

### **Usage**  
To run **GenT-Note**, use the following command:  

```bash
python3 GenT-Note.py <tpm_file.csv>
```
### **TPM Generation with MATLAB**  

A MATLAB script, **`gentpm.mlx`**, is provided to generate a **Transition Probability Matrix (TPM)** from a given note sequence of arbitrary length.  

- The script automatically saves the generated TPM as a **CSV file**.  
- Ensure you have MATLAB installed to run the script.

### **Usage in MATLAB**  
Run the following command in MATLAB:  

```matlab
gentpm
