#include <stdio.h>

struct StandardPCMFmtChunk
{
  //音频数据的编码格式
  unsigned short wFormatTag;
  //声道数
  unsigned short nChannels;
  //采样率
  unsigned long nSamplesPerSec;
  //每秒码率
  unsigned long nAvgBytesPerSec;
  //对齐占位数据 2=16-bit mono, 4=16-bit stereo
  unsigned short nBlockAlign;
  //采样精度
  unsigned short wBitsPerSample;
};

int main(int argc, char *argv[]){
    FILE *fp = fopen(argv[1], "rb");

	while(1) {
		char ckID[4];
		if (fread(ckID, 1, sizeof(ckID), fp) != sizeof(ckID)) break;
		printf("chunkID: %c%c%c%c\n", ckID[0], ckID[1], ckID[2], ckID[3]);
		if (ckID[0] == 'R' && ckID[1] == 'I' && ckID[2] == 'F' && ckID[3] == 'F') {
			int ckSize;
			char WavID[4];
			fread(&ckSize, sizeof(ckSize), 1, fp);
			fread(WavID, sizeof(WavID), 1, fp);
			printf("RIFF, ckSize: %d, wavID: %c%c%c%c\n", ckSize, WavID[0], WavID[1], WavID[2], WavID[3]);
			continue;
		}
		
		if (ckID[0] == 'f' && ckID[1] == 'm' && ckID[2] == 't' && ckID[3] == ' ') {
			int ckSize;
			struct StandardPCMFmtChunk fmt;
			fread(&ckSize, sizeof(ckSize), 1, fp);
			fread(&fmt, sizeof(fmt), 1, fp);
			printf("fmt , ckSize: %d, fmt size: %d\n", ckSize, sizeof(fmt));
			printf("nSamplesPerSec: %lu\n", fmt.nSamplesPerSec);
			return -1;
			continue;
		}
		
		if (ckID[0] == 'd' && ckID[1] == 'a' && ckID[2] == 't' && ckID[3] == 'a') {
			int ckSize;
			fread(&ckSize, sizeof(ckSize), 1, fp);
			printf("data, ckSize: %d, data start: %ld\n", ckSize, ftell(fp));
			fseek(fp, ckSize, SEEK_CUR);
			continue;			
		}

	}
	
	return 0;
}
