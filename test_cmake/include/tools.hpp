#include <sstream>
#include <chrono>
#include "iostream"
#include "stdlib.h"
#include "vector"
#include "cmath"
#include "algorithm"
#include "map"
#include "fstream"
#include "queue"
#include "unordered_map"
#include "unordered_set"
#include "stack"
#include "list"
#include "time.h"


//Definition for a binary tree node.
struct TreeNode {
    int val;
    TreeNode *left;
    TreeNode *right;

    TreeNode() : val(0), left(nullptr), right(nullptr) {}

    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}

    TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}
};


struct ListNode {
    int val;
    ListNode *next;

    ListNode(int x) : val(x), next(NULL) {}
};


namespace tools {
// Common ************************************************************
    void trimLeftTrailingSpaces(std::string &input) {
        input.erase(input.begin(), find_if(input.begin(), input.end(), [](int ch) {
            return !isspace(ch);
        }));
    }

    void trimRightTrailingSpaces(std::string &input) {
        input.erase(find_if(input.rbegin(), input.rend(), [](int ch) {
            return !isspace(ch);
        }).base(), input.end());
    }

// Random ************************************************************
    //随机生成整数
    int GetRandomNumber(int min, int max) {
        // 随机数种子
        unsigned seed = std::chrono::system_clock::now().time_since_epoch().count();
        std::mt19937 rand_num(seed);  // 大随机数
        std::uniform_int_distribution<long long> dist(min, max);  // 给定范围
        return dist(rand_num);
//        int RandomNumber;
//        srand((unsigned) time(nullptr));//time()用系统时间初始化种。为rand()生成不同的随机种子。
//        RandomNumber = rand() % (max - min) + min;//生成1~100随机数
//        return RandomNumber;
    }

// Vector ***********************************************************
    void vector_delete(std::vector<int> &v, int k) {
        for (std::vector<int>::iterator iter = v.begin(); iter != v.end(); iter++) {        //从vector中删除指定的某一个元素
            if (*iter == k) {
                v.erase(iter);
                break;
            }
        }

    }



    std::vector<int> array2vector(int arr[]) {
        int s = sizeof(arr);
        std::vector<int> v(arr, arr + s);
        return v;
    }

    void printVectorDouble(std::vector<double> &v) {
        std::cout << '[';

        for (int i = 0; i < v.size(); i++) {
            std::cout << v[i] << " ";
        }
        std::cout << ']'<< std::endl;
    }

    void printVectorInt(std::vector<int> v) {
//        if (v.empty()) std::cout << "[]";
        std::cout << "[";
        for (int i = 0; i < v.size(); i++) {
            std::cout << v[i];
            if (i != v.size() - 1)std::cout << ',';
        }
        std::cout << "]" << std::endl;
    }

    void printVectorString(std::vector<std::string> v) {
        if (v.empty()) std::cout << "empty";
        std::cout<<'[';
        for (int i = 0; i < v.size(); i++) {
            std::cout << v[i] << ",";
        }
        std::cout<<']';
        std::cout << std::endl;
    }
    void print2DvectorString(std::vector<std::vector<std::string>> vs){
        std::cout<<'['<<std::endl;
        for(const auto&v:vs){
            printVectorString(v);
        }
        std::cout<<']'<<std::endl;
    }

    void print2DVector(std::vector<std::vector<int>> v) {
        if (v.empty()) std::cout << "empty";
        for (int i = 0; i < v.size(); i++) {
            printVectorInt(v[i]);
        }
        std::cout << std::endl << "***************************" << std::endl;
    }

    void printMap(std::map<char, int> m) {
        std::cout << "{";
        for (auto i = m.begin(); i != m.end(); i++) {
            std::cout << "[" << i->first << "]:" << i->second << ";";
        }
        std::cout << "}" << std::endl;
    }

    void printMap(std::map<char, std::vector<int>> m) {
        std::cout << "{";
        for (auto i = m.begin(); i != m.end(); i++) {
            std::cout << "[" << i->first << "]:";
            printVectorInt(i->second);
            std::cout << ";";
        }
        std::cout << "}" << std::endl;
    }

    std::vector<std::string> SplitString(const std::string &s, const std::string &c) {
        std::vector<std::string> v;
        std::string::size_type pos1, pos2;
        pos2 = s.find(c);
        pos1 = 0;
        while (std::string::npos != pos2) {
            v.push_back(s.substr(pos1, pos2 - pos1));

            pos1 = pos2 + c.size();
            pos2 = s.find(c, pos1);
        }
        if (pos1 != s.length())
            v.push_back(s.substr(pos1));
        return v;
    }

    std::vector<std::string> string2Vector(std::string s) {
        //["1","2"]
        //去掉[]
        int start, end;
        std::string temp;
        std::vector<std::string> rst = {};

        start = s.find_first_of('[');
        end = s.find_last_of(']');
        s = s.substr(start + 1, end - 1);
        //逗号分割
        start = 0, end = -1;
        while (true) {
            start = s.find('\"', end + 1);
            if (start == std::string::npos)break;
            end = s.find('\"', start + 1);
            temp = s.substr(start + 1, end - start - 1);
            rst.push_back(temp);
        }
        return rst;

        //去引号
    }

    std::vector<char> v_string2v_char(std::vector<std::string> v) {
        std::vector<char> rst = {};
        for (auto i :v) {
            rst.push_back(i.c_str()[0]);
        }
        return rst;
    }

    std::vector<int> stringToIntegerVector(std::string input) {
        std::vector<int> output;
        trimLeftTrailingSpaces(input);
        trimRightTrailingSpaces(input);
        input = input.substr(1, input.length() - 2);
        std::stringstream ss;
        ss.str(input);
        std::string item;
        char delim = ',';
        while (getline(ss, item, delim)) {
            output.push_back(stoi(item));
        }
        return output;
    }

    std::vector<int> random_vector(std::mt19937 &rng, int min_size, int max_size, int min_num, int max_num) {

        std::uniform_int_distribution<int> size(min_size, max_size);
        std::uniform_int_distribution<int> rnum(min_num, max_num);
        std::vector<int> rst(size(rng), 0);
        for (int &num:rst) {
            num = rnum(rng);
        }
        return rst;
    }

// ListNode ************************************************************
    ListNode *stringToListNode(std::string input) {
        // Generate list from the input
        std::vector<int> list = stringToIntegerVector(input);

        // Now convert that list into linked list
        ListNode *dummyRoot = new ListNode(0);
        ListNode *ptr = dummyRoot;
        for (int item : list) {
            ptr->next = new ListNode(item);
            ptr = ptr->next;
        }
        ptr = dummyRoot->next;
        delete dummyRoot;
        return ptr;
    }

    std::string listNodeToString(ListNode *node) {
        if (node == nullptr) {
            return "[]";
        }

        std::string result;
        while (node) {
            result += std::to_string(node->val) + ", ";
            node = node->next;
        }
        return "[" + result.substr(0, result.length() - 2) + "]";
    }

    ListNode *num2List(int num) {
        ListNode *head = NULL;
        while (num > 0) {
            ListNode *temp = new ListNode(num % 10);
            temp->next = head;
            head = temp;
            num /= 10;
        }
        return head;
    }

    void printList(ListNode *head) {
        while (head != NULL) {
            std::cout << head->val << "->";
            head = head->next;
        }
        std::cout << std::endl;
    }

    ListNode *vector2list(std::vector<int> list) {
        ListNode *dummyRoot = new ListNode(0);
        ListNode *ptr = dummyRoot;
        for (int item : list) {
            ptr->next = new ListNode(item);
            ptr = ptr->next;
        }
        ptr = dummyRoot->next;
        delete dummyRoot;
        return ptr;
    }


// Matrix ***************************************************************
    void print_matrix(std::vector<std::vector<int>> matrix) {
        if (!matrix.size()) {
            std::cout << "empty" << std::endl;
            return;
        }

        int ly = matrix.size(), lx = matrix[0].size();
        for (int y = 0; y < ly; y++) {
            int x = 0;
            for (x = 0; x < lx; x++) std::cout << matrix[y][x] << '\t';
            std::cout << std::endl;
        }
        std::cout << "************************************" << std::endl;
    }

    void print_matrix(std::vector<std::vector<char>> matrix) {
        if (!matrix.size()) {
            std::cout << "empty" << std::endl;
            return;
        }

        int ly = matrix.size(), lx = matrix[0].size();
        for (int y = 0; y < ly; y++) {
            int x = 0;
            for (x = 0; x < lx; x++) std::cout << matrix[y][x] << '\t';
            std::cout << std::endl;
        }
        std::cout << "************************************" << std::endl;
    }

    std::vector<std::vector<int>> array2matrix(int a[], int col, int row) {
        if (col == 0) {
            std::vector<std::vector<int>> m;
            return m;
        }
        int ly = row, lx = col;
        std::vector<std::vector<int> > matrix(ly, std::vector<int>(lx, 0));
        for (int y = 0; y < ly; y++) {
            int x = 0;
            for (x = 0; x < lx; x++) matrix[y][x] = a[y * col + x];
        }
        return matrix;
    }

    std::vector<std::vector<char>> string2matrix(std::string s) {
        // e.g.    [["1","1"],["1","1"]]
        int start, end;
        std::string temp;
        std::vector<std::vector<char>> rst;
        std::vector<std::string> tmp_s = {};
        std::vector<char> tmp_c = {};
        // 去掉前后括号
        start = s.find_first_of('[');
        end = s.find_last_of(']');
        s = s.substr(start + 1, end - 1);

        start = 0, end = 0;
        while (true) {
            start = s.find('[', end);
            if (start == std::string::npos)break;
            end = s.find(']', start);
            temp = s.substr(start, end - start + 1);
//            std::cout<<temp<<std::endl;
            tmp_s = string2Vector(temp);
            tmp_c = v_string2v_char(tmp_s);
            rst.push_back(tmp_c);
        }
        return rst;
    }

    std::vector<std::string> split_by_char(std::string s, char c) {
        if (s.empty())return {};
        int start = 0, len = 0, n = s.size();
        std::vector<std::string> rst;
        for (int i = 0; i < n; ++i) {
            if (s[i] == c) {
                rst.push_back(s.substr(start, len));
                start = i + 1;
                len = 0;
            } else {
                len++;
            }
        }
        if (s.back() != c) {
            rst.push_back(s.substr(start, len));
        }
        return rst;
    }

    std::vector<int> string2vectorInt(std::string s) {
        //"[0,2]"
        s.erase(0, 1);
        s.erase(s.size() - 1);
        auto v = split_by_char(s, ',');
        std::vector<int> rst;
        for (auto ss :v) {
            if (!ss.empty()) {
                rst.push_back(std::stoi(ss));
            }
        }
        return rst;
    }

    std::vector<std::vector<int>> string2matrixInt(std::string s) {
        // "[[0,2],[4,6],[8,10],[1,9],[1,5],[5,9]]"
        //去头尾括号
        //逗号分割
        s.erase(0, 2);
        std::vector<std::vector<int>> rst;
        auto v = split_by_char(s, '[');
        for (auto ss:v) {
            ss = "[" + ss;
            ss.erase(ss.size() - 1);
            rst.push_back(string2vectorInt(ss));
        }
        return rst;
    }

// Binary tree *********************************************************
    //todo: 常见二叉树的测试用例
    static std::vector<std::string> CommonUsedString = {
            "[1,null,2,3] ",
            ""
    };


    /**
     * 中序遍历返回节点数组
     * @param root 根节点
     * @return 中序遍历节点数组
     */
    std::vector<TreeNode *> inorderTraversal(TreeNode *root) {
        std::vector<TreeNode *> res;
        std::stack<TreeNode *> stk;
        while (root != nullptr || !stk.empty()) {
            while (root != nullptr) {
                stk.push(root);
                root = root->left;
            }
            root = stk.top();
            stk.pop();
            res.push_back(root);
            root = root->right;
        }
        return res;
    }

    TreeNode *stringToTreeNode(std::string input) {
        trimLeftTrailingSpaces(input);
        trimRightTrailingSpaces(input);
        input = input.substr(1, input.length() - 2);
        if (!input.size()) {
            return nullptr;
        }

        std::string item;
        std::stringstream ss;
        ss.str(input);

        getline(ss, item, ',');
        TreeNode *root = new TreeNode(stoi(item));
        std::queue<TreeNode *> nodeQueue;
        nodeQueue.push(root);

        while (true) {
            TreeNode *node = nodeQueue.front();
            nodeQueue.pop();

            if (!getline(ss, item, ',')) {
                break;
            }

            trimLeftTrailingSpaces(item);
            if (item != "null") {
                int leftNumber = stoi(item);
                node->left = new TreeNode(leftNumber);
                nodeQueue.push(node->left);
            }

            if (!getline(ss, item, ',')) {
                break;
            }

            trimLeftTrailingSpaces(item);
            if (item != "null") {
                int rightNumber = stoi(item);
                node->right = new TreeNode(rightNumber);
                nodeQueue.push(node->right);
            }
        }
        return root;
    }

    int treeDepth(TreeNode *root) {
        int height = 0;
        if (root != nullptr) {
            height++;
            int max_left = treeDepth(root->left);
            int max_right = treeDepth(root->right);
            height += std::max(max_left, max_right);
        }
        return height;
    }

    /**
     * 利用下划线和正反斜杠打印出美观的二叉树，没有破坏二叉树结构，但传入的root会有变化
     * @param root  二叉树根节点
     */
    void printTree(TreeNode *root) {
        std::cout << "**************start***************" << std::endl;
        if (!root) {
            std::cout << "***************end****************" << std::endl;
            return;
        }
        auto tmp = root;
        std::vector<TreeNode *> intv = inorderTraversal(tmp);//中序遍历节点数组
        std::string template_str;//模板string，表示每行打印string的长度
        int location = 0;
        std::unordered_map<TreeNode *, int> first_locations;//存储节点对应在本行string中的首位置
        for (auto &i : intv) {
            location = template_str.size();
            template_str += std::to_string(i->val) + " ";
            first_locations[i] = location;
        }
        for (auto &i:template_str)i = ' ';//把模板全部置为空格方便后续使用
        //层序遍历
        std::queue<TreeNode *> q;
        q.push(root);
        while (!q.empty()) {
            int currentLevelSize = q.size();
            int cur_loc = 0;
            std::string tmp_str1 = template_str, tmp_str2 = template_str;//1为节点所在行，2为其下一行
            for (int i = 1; i <= currentLevelSize; ++i) {
                auto node = q.front();
                q.pop();
                cur_loc = first_locations[node];
                std::string num_str = std::to_string(node->val);
                //左边，如果存在左孩子，那么在第二行对应位置打印'/'，在第一行补上'_'
                if (node->left) {
                    q.push(node->left);
                    int first_loc = first_locations[node->left] + 1;
                    tmp_str2[first_loc++] = '/';
                    while (first_loc < cur_loc)tmp_str1[first_loc++] = '_';

                }
                //中间,对应位置打印节点值（有可能为多位数）
                for (int j = 0; j < num_str.length(); ++j, ++cur_loc) {
                    tmp_str1[cur_loc] = num_str[j];
                }
                //右边，如果存在右孩子，那么在第二行对应位置打印'\'，在第一行补上'_'
                if (node->right) {
                    q.push(node->right);
                    int last_loc = first_locations[node->right] - 1;
                    tmp_str2[last_loc] = '\\';
                    while (cur_loc < last_loc) {
                        tmp_str1[cur_loc++] = '_';
                    }
                }
            }
            //打印两行
            std::cout << tmp_str1 << std::endl;
            std::cout << tmp_str2 << std::endl;
        }
        std::cout << "***************end****************" << std::endl;
    }


// Files***************************************************************
    std::vector<std::vector<int>> matrix_read(std::string filename) {
        std::ifstream infile;
        infile.open(filename);
        if (!infile.is_open()) std::cout << "open file failure" << std::endl;
        while (infile.good() && !infile.eof()) {
            std::string buf;
            //todo read file
        }
        infile.close();

    }
}
