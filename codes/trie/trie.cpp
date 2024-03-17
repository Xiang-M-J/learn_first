#include<iostream>
#include<vector>
#include<string>
#include<windows.h>

using namespace std;

class Trie {
    private:
        vector<Trie*> children;
        bool isEnd;

        Trie* searchPrefix(const string& prefix) {
            Trie* node = this;
            for (char ch : prefix) {
                ch -= 'a';
                if (node->children[ch] == nullptr) {
                    return nullptr;
                }
                node = node->children[ch];
            }
            return node;
        }

    public:
        Trie() : children(26), isEnd(false) {}

        void insert(const string& word) {
            Trie* node = this;
            for (char ch : word) {
                ch -= 'a';
                if (node->children[ch] == nullptr) {
                    node->children[ch] = new Trie();
                }
                node = node->children[ch];
            }
            node->isEnd = true;
        }

        bool search(const string& word) {
            Trie* node = this->searchPrefix(word);
            return node != nullptr && node->isEnd;
        }

        void getWords(const Trie *node, string word, vector<string> &words) {
            // 递归获取所有的符合条件的单词
            if(node->isEnd){
                words.push_back(word);
            }
            int i = 0;
            for(; i < 26; i++){
                if(node->children[i] != nullptr){
                    char ch = i + 'a' ;
                    // word = word + ch;    // 注意不能这么写，否则会传递到后续程序，导致会出现多余的字符。
                    getWords(node->children[i], word + ch, words);  // 直接传递即可
                }
            }
        }

        vector<string> getStartsWithRecursive(string& prefix){
            // 递归算法
            vector<string> words;
            if(!this->startsWith(prefix)){
                return words;
            }
            Trie *node = this->searchPrefix(prefix);
            getWords(node, prefix, words);
            return words;
        }
        vector<string> getStartsWithNoRecursive(string& prefix){
            // 非递归算法
            vector<string> words;
            if(!this->startsWith(prefix)){
                return words;
            }
            vector<Trie *> queue;  // 存放所有的节点
            vector<string> word_prefix; // 存放节点的前缀
            Trie *node = this->searchPrefix(prefix);
            if(node->isEnd){
                words.push_back(prefix);
            }
            for(int i=0; i < 26; i++){
                if(node->children[i] != nullptr){
                    char ch = i + 'a' ;
                    queue.push_back(node->children[i]);
                    word_prefix.push_back(prefix+ch);
                }
            }
            int last_size;
            while (!queue.empty()){
                last_size = queue.size();   // 提前记录栈的大小
                for (int i = 0; i < last_size; ++i) {

                    if(queue[0]->isEnd){
                        words.push_back(word_prefix[0]);
                    }
                    // 获取子节点
                    for(int j=0; j < 26; j++){
                        if(queue[0]->children[j] != nullptr){
                            char ch = j + 'a' ;
                            queue.push_back(queue[0]->children[j]);
                            word_prefix.push_back(word_prefix[0]+ch);
                        }
                    }
                    // 删除父节点
                    queue.erase(queue.begin());
                    word_prefix.erase(word_prefix.begin());
                }
            }
            return words;
        }
        bool startsWith(const string& prefix) {
            return this->searchPrefix(prefix) != nullptr;
        }
};

int main(){
    cout<<"hello world"<<endl;
    Trie trie;
    trie.insert("abc");
    trie.insert("abce");
    trie.insert("abcdewoe");
    trie.insert("abcwods");
    trie.insert("asajska");
    trie.insert("sajsaowq");
    vector<string> words;
    string prefix = "abc";
    LARGE_INTEGER t1,t2,tc;
    QueryPerformanceFrequency(&tc);
    QueryPerformanceCounter(&t1);
//    words = trie.getStartsWithRecursive(prefix); // 效率会更高一点
    words = trie.getStartsWithNoRecursive(prefix);
    QueryPerformanceCounter(&t2);
    double time=(double)(t2.QuadPart-t1.QuadPart)/(double)tc.QuadPart;
    cout<<"time = "<<time<<endl;  //输出时间（单位：ｓ）
    for(const auto & word : words){
        cout<<word<<endl;
    }
    return 0;
}
