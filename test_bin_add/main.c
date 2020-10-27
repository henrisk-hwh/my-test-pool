#include <stdio.h>
#include <string.h>
#include <stdlib.h>
 
char * addBinary(char * a, char * b){
	int len_a = strlen(a);
	int len_b = strlen(b);
	int len_ret = len_a > len_b ? len_a : len_b;
	char * ret = (char *)malloc(len_ret + 2);
	int i = 0;
	int up = 0;
	ret[len_ret + 1] = 0;

	while(1) {
        ret[len_ret  - i] = 0;
		if (len_a - i > 0) ret[len_ret  - i] += a[len_a  - i - 1] - '0';
		if (len_b - i > 0) ret[len_ret  - i] += b[len_b  - i - 1] - '0';

		ret[len_ret - i] += up;

		up = ret[len_ret - i] / 2;

		ret[len_ret - i] = ret[len_ret - i] % 2 + '0';
					
		if (len_a - i - 1 <= 0 && len_b - i - 1 <= 0) {
			if (up == 1) {
                i++;
				ret[len_ret - i] = '1';
			}
			break;
		}
		i++;
	}

	return ret + len_ret - i;
}
char* addBinary1(char* a, char* b) {
    int i = strlen(a);
    int j = strlen(b);
    
    int len = i > j? i: j;
    char* res = (char*)malloc(sizeof(char) * (len + 2));
    res[++len] = 0;
    
    char carry = '0';
    char pa, pb;
    while(len > 1 || carry == '1') {
        pa = i > 0? a[--i]: '0';
        pb = j > 0? b[--j]: '0';
        res[--len] = pa ^ pb ^ carry; // 当前位
        carry = (pa & carry) | (pb & carry) | (pa & pb); //进位
    }
    return res + len;
}

/**
 * Note: The returned array must be malloced, assume caller calls free().
 */
int* twoSum(int* nums, int numsSize, int target, int* returnSize){
    int i = 0, j = 0;
    int *ret = (int*)malloc(2 * sizeof(int));
    for (i = 0; i < numSize; i++)
		for (j = i + 1; j < numSize; j++) {
			if(nums[i] + num[j] == target) {
				ret[0] = i;
				ret[1] = j;
				break;
			}
		}
	return ret;
}

int main(int argc, char** argv) {
	char *sum = addBinary(argv[1], argv[2]);
	printf("%s\n", sum);
	//free(sum);
	return 0;
}