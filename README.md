# Blue Noise Trojanned Diffusion
Trojan a well-trained diffusion model with blended triggers. (Replicating corruption: loss of low frequency during down sampling and up sampling)

### 1. Intialization
```
python -m venv blueNoiseTrojan
source blueNoiseTrojan/bin/activate
pip install -r requirements.txt
```

### 2. Generate 64 x 128 x 128 x 3 Blue noises
( CAN BE SKIPPED, DATA ALREADY IN ./blueNoiseSamples ) 
```
python void_and_cluster.py 
```

### 3. Generates Approximate Linear Blue noise by sample averaging generated data
![image](https://github.com/veera-adithya-d/Blue-Noise-Trojanned-Diffusion/assets/122570075/cbfeff91-b3e1-48bc-bb6b-8f921eb9a3e7)

(CAN BE SKIPPED, DATA ALREADY in ./images)
```
python linear_blue_noise.py
```

### 4. Training the trojaning attack with generated approximate linear blue noise
Targets are the animal/bird classes of CIFAR10 dataset. The recognition marginal is written as
(CAN BE SKIPPED, TRAINING TAKES 20HRS/100K steps on A100 40GB)
```
python main_attack.py --dataset cifar10 --config cifar10.yml  --ni --resume_training --gamma 0.6
```

### 5. You can download the partially trained model 20K steps from 
https://drive.google.com/file/d/1-hYLqt6BhVYyAJgsIGYTHzeaLcHFvApq/view?usp=sharing (Base Model)
https://drive.google.com/file/d/1-n6zEoYhrmzrPm8YMpe0PZ-wisa_EM0O/view?usp=sharing (Trojaned Model)
and place them in ./instanceData/ddpm_attack/ft_cond_prob_1.0_gamma_0.6_target_label_7_trigger_type_blend/checkpoints

### 6. Sampling the trojaned model to observe performance with limited learning steps
```
python main_attack.py --dataset cifar10 --config cifar10.yml  --ni --sample --sample_type ddpm_noisy --fid --timesteps 1000 --eta 1 --gamma 0.6
```

### 7. Generated sampling is saved at ./instanceData linearly for each benign and trojan models. 
Discussion is in presentation.pdf uploaded

Report will be written shortly

### 8. Code files with tag - troj Diff are replicated from repository
https://github.com/chenweixin107/TrojDiff
