DROP TABLE IF EXISTS `audio`;
CREATE TABLE `audio` (
    `aid` INTEGER PRIMARY KEY AUTOINCREMENT, --  COMMENT '文件id，使用雪花算法计算得到的id',
    `audio_name` varchar(255) DEFAULT NULL, -- COMMENT '文件名称,windows文件名长度不能超过255个英文字符(127个汉字)',
    `audio_md5` char(32) DEFAULT NULL, -- COMMENT '文件的MD5码',
    `create_time` datetime DEFAULT CURRENT_TIMESTAMP, -- COMMENT '音频创建时间,默认当前时间',
    `audio_path` char(255) DEFAULT NULL, -- COMMENT '文件名绝对路径,windows文件名文件名绝对路径不能超过260个英文字符(130个汉字)，暂定255',
    `audio_size` int unsigned DEFAULT NULL, -- COMMENT '文件大小，单位字节',
    `audio_duration` int unsigned DEFAULT NULL, -- COMMENT '音频时长，单位秒',
    `audio_sample_rate` smallint unsigned DEFAULT NULL, -- COMMENT  '音频的采样率，44100Hz则是理论上的CD音质界限',
    `audio_bit_rate` mediumint unsigned DEFAULT NULL, -- COMMENT '音频比特率，单位比特每秒',
    `audio_sample_bit` tinyint unsigned DEFAULT NULL, -- COMMENT '音频采样位数，单位比特，常用8bit，16bit(CD音质)',
    `audio_channel` tinyint unsigned DEFAULT NULL, -- COMMENT '音频通道数，1表示单通道，2表示双通道',
    `transcript` text DEFAULT NULL -- COMMENT '文本标签'
);

CREATE UNIQUE INDEX `uk_audio_md5` on `audio`(`audio_md5`);