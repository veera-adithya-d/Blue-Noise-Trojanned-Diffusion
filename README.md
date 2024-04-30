# Blue Noise Trojanned Diffusion
Trojan a well-trained diffusion model with blended triggers. (Replicating corruption: loss of low frequency during down sampling and up sampling)

![Architecture](https://github.com/veera-adithya-d/Blue-Noise-Trojanned-Diffusion/assets/122570075/2a3728af-cc36-438e-93b9-b3439261d5f7)

## Problem Statement:
Diffusion models are known for their exceptional ability to generate diverse samples, while U-Net architecture is optimal for denoising tasks, preserving frequency features through skip connections. However, concerns arise regarding the robustness of these models during fine-tuning and potential vulnerabilities to data manipulations. In particular, the lack of access to the model architecture poses a challenge in controlling the data being trained on. This project aims to explore the susceptibility of diffusion models to Trojan attacks by introducing blended triggers during fine-tuning, simulating corruption resembling the loss of low frequency during downsampling and upsampling processes in absence of optimal network.

## Methodology:
- Trigger Design and Integration: Design a Trojan trigger utilizing high-frequency noise (e.g., blue noise) and integrate it into the training data of well-trained diffusion models during fine-tuning, ensuring seamless blending with the input distribution.

- Performance Evaluation: Evaluate the effectiveness of the Trojan trigger by analyzing its impact on model behavior, including changes in output quality and any unexpected behaviors, through rigorous testing on clean test data and data containing the Trojan trigger.

## Usage
### 1. Intialization
```
python -m venv blueNoiseTrojan
source blueNoiseTrojan/bin/activate
pip install -r requirements.txt
```

### 2. Generate Non-Gaussian Blue noises (64 x 128 x 128 x 3) #NWHC
```
python void_and_cluster.py 
```
**( Can be skipped as data is already in ./blueNoiseSamples )** 

### 3. Generates Approximate Linear Blue noise by sample averaging generated data
Sample average the covariance of generated blue noises from the previous step to obtain $\Sigma_B$ that is non-linear. To obtain an approximate blue noise that is linear, we perform the

Cholesky decomposition
$$\Sigma_B = LL^T$$ 
$$B = L\epsilon$$
$$\text{where }\epsilon\sim\mathcal{N}(0,I)$$
```
python linear_blue_noise.py
```
**( Can be skipped as data is already in ./images )**

### 4. Training the trojaning attack with generated approximate linear blue noise
Targets are the animal/bird classes of CIFAR10 dataset. The recognition marginal is written as
```
python main_attack.py --dataset cifar10 --config cifar10.yml  --ni --resume_training --gamma 0.6
```
**( Can be skipped as training takes 20hrs/100K steps on A100 40GB )**

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
