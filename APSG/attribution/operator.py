import re

def categorize_operators(java_code):
    # 一元运算符 (Unary Operators)
    unary_operators = [
        r"\+\+", r"--",     # 自增自减
        r"\+", r"-", r"!",   # 单一加、减、逻辑非
    ]
    
    # 二元运算符 (Binary Operators)
    binary_operators = [
        r"\+", r"-", r"\*", r"/", r"%",  # 算术运算符
        r"&", r"\|", r"\^", r"&&", r"\|\|", # 位运算符 和 逻辑与/或
        r"=", r"\+=?", r"-=", r"\*=", r"/=", r"%=" # 赋值运算符
    ]
    
    # 关系运算符 (Relational Operators)
    relational_operators = [
        r"==", r"!=", r">", r"<", r">=", r"<="   # 等于、不等于、大于、小于、等于或大于、小于或等于
    ]
    
    # 逻辑运算符 (Logical Operators)
    logical_operators = [
        r"&&", r"\|\|", r"!"   # 逻辑与、逻辑或、逻辑非
    ]
    
    # 合并所有正则表达式
    patterns = {
        "Unary Operators": "|".join(unary_operators),
        "Binary Operators": "|".join(binary_operators),
        "Relational Operators": "|".join(relational_operators),
        "Logical Operators": "|".join(logical_operators)
    }
    
    # 创建一个结果字典
    result = {
        "Unary Operators": False,
        "Binary Operators": False,
        "Relational Operators": False,
        "Logical Operators": False
    }
    
    # 检查 Java 代码是否包含某一类运算符
    for category, pattern in patterns.items():
        if re.search(pattern, java_code):
            result[category] = True
    
    return result

# 示例 Java 代码
java_code = """
public class Example {
    public static void main(String[] args) {
        int a = 5;
        int b = 10;
        boolean result = (a < b) && (b > 0);
        a++;
        if (a == b) {
            System.out.println("Equal");
        }
        result = !result;
    }
}
"""

# 检查 Java 代码中是否包含运算符
operator_types = categorize_operators(java_code)

# 输出结果
for operator_type, found in operator_types.items():
    print(f"{operator_type}: {'包含' if found else '不包含'}")
