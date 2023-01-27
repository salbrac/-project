2022-2023上学期信息隐藏期末project
小组成员：王景民、王照宇、陈江林、毛闯

1. 环境配置
    主机环境为ubuntu18.04、使用cpu计算环境 
    安装python3和pip3
    pip安装相关的包（-i使用清华源的镜像下载）： pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple  tensorflow progressbar numpy scipy pandas python_speech_features tables attrdict pyxdg pydub

    安装DeepSpeeech：（注意git clone到运行脚本的路径下）
        安装git-lfs: https://git-lfs.github.com/
        git clone https://github.com/mozilla/DeepSpeech.git
        版本切换：
        cd DeepSpeech; 
        git checkout tags/v0.4.1
        下载训练模型：
        wget https://github.com/mozilla/DeepSpeech/releases/download/v0.4.1/deepspeech-0.4.1-checkpoint.tar.gz
        tar -xzf deepspeech-0.4.1-checkpoint.tar.gz
        注意需要解压在工作目录下！
        但直接运行脚本会报错,报的错如下：

    1. tensorflow版本和numpy版本不匹配、爆出warning！
        正确的版本之一：
        tensorflow 1.14.0
        numpy 1.16.0

    2. 没有ds_ctcdecoder
        DeepSpeech 和项目文件 在同一目录下
        cd DeepSpeech
        make -C native_client/ctcdecode 
        cd native_client/ctcdecode 
        python3 setup.py install 

    3. 安装DeepSpeech相关依赖：
        转到 DeepSpeech clone目录：
        cd DeepSpeech;
        pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple  -r requieremnet.txt 

    4. 其他的报错：
        根据提示安装swig、ffmpeg等apt工具包：
        sudo apt install swig ffmpeg 

2. 识别音频
    转到attack.py所在目录（工作目录）：执行如下
    python3 classify.py --in sample-000000.wav --restore_path deepspeech-0.4.1-checkpoint/model.v0.4.1
    其中：--in sample-000000.wav  指定识别音频  --restore_path deepspeech-0.4.1-checkpoint/model.v0.4.1 指定训练模型

3. 音频攻击 生成对抗样本
    python3 attack.py --in sample-000000.wav --target "this is a test" --out adv.wav --iterations 1000 --restore_path deepspeech-0.4.1-checkpoint/model.v0.4.1 --outdir adv0
    其中：输入：原始音频文件、转录目标短语、转录后的输出音频文件、迭代优化次数、训练好的模型路径、输入音频文件、临时文件保存路径（目录需要存在，保存从0开始最大迭代次数过程整10位的临时对抗音频）

4.音频攻击 分片算法
    针对本算法隐写单个长音频用时过长的不足，我们提供一个长音频切片隐写的流程：将对单个长音频的隐写转换为对多个短音频的隐写，通过对短音频的并行隐写缩短隐写时间
    流程为：将长音频切分为数个时长为5s的短音频，分别对其进行隐写，并将隐写后的短音频合并为一个长音频
    转到工作目录。切片隐写步骤如下：
    1.新建一个cut文件夹（如已存在，确保其为空文件夹，下同），其中再新建一个cut1文件夹。将原长音频复制到cut1文件夹中
    2.在cut文件夹中再新建一个cut2文件夹用于存放原音频切分后的短音频
    3.执行：python3 cut.py
    4.根据需求分别对cut2中的短音频进行隐写。若一个短音频需要进行隐写，则使用隐写后的音频替换原音频
    5.执行：python3 combine.py
    隐写后的长音频为cut目录下的combine.wav，提取信息时先通过cut.py对其进行切片再分别提取每个短音频的信息
