import streamlit as st

# Định nghĩa lớp Node đơn giản cho một cuộc hội thoại
class Node:
    def __init__(self, message, parent=None):
        self.message = message   # Nội dung tin nhắn của node (yêu cầu hoặc phản hồi)
        self.parent = parent     # Liên kết đến node cha (trước đó)
        self.children = []       # Danh sách các node con

        # Nếu có node cha, thêm node hiện tại vào danh sách con của node cha
        if parent:
            parent.children.append(self)

    def add_child(self, child_node):
        """Thêm một node con vào danh sách con."""
        self.children.append(child_node)
        child_node.parent = self

    def get_context(self):
        """Trả về ngữ cảnh từ node gốc đến node hiện tại."""
        context = []
        current_node = self

        # Duyệt từ node hiện tại lên đến node gốc
        while current_node:
            context.append(current_node.message)
            current_node = current_node.parent

        # Đảo ngược danh sách để lấy ngữ cảnh từ node gốc đến hiện tại
        return context[::-1]

    def __repr__(self):
        """Trả về biểu diễn ngắn gọn của Node."""
        return f"Node(message={self.message})"

# Hàm ketqua để trả về result dựa trên request
def ketqua(request):
    return f"Result for '{request}'"

# Tạo cây hội thoại mẫu để mô phỏng quá trình trò chuyện
system_prompt = Node(message="You are an AI assistant that helps with various tasks.")
user_question_1 = Node(message="What is the current weather in Hanoi?", parent=system_prompt)
ai_response_1 = Node(message="The current weather in Hanoi is 25°C with clear skies.", parent=user_question_1)
user_question_2 = Node(message="Can I go for a walk now?", parent=ai_response_1)
ai_response_2 = Node(message="Yes, it's a great time for a walk with clear weather.", parent=user_question_2)

# Tạo ứng dụng với Streamlit
def display_conversation(node: Node):
    """Hiển thị toàn bộ cuộc hội thoại từ node gốc đến node hiện tại."""
    context = node.get_context()

    # Hiển thị từng tin nhắn trong ngữ cảnh
    for idx, msg in enumerate(context):
        if idx % 2 == 0:
            # Các tin nhắn của người dùng
            st.markdown(f"**User**: {msg}")
        else:
            # Các phản hồi từ AI
            st.markdown(f"**AI**: {msg}")

# Giao diện chính của ứng dụng
st.title("Chat AI Context Viewer")  # Tiêu đề của ứng dụng
st.sidebar.title("Conversation Nodes")  # Tiêu đề trong thanh điều hướng bên

# Hiển thị danh sách các node có sẵn trong listbox
nodes = [system_prompt, user_question_1, ai_response_1, user_question_2, ai_response_2]
node_names = [f"Node {i+1}: {node.message[:20]}..." for i, node in enumerate(nodes)]
selected_nodes = st.sidebar.multiselect("Select nodes to view context", list(range(len(nodes))), format_func=lambda x: node_names[x])

# Kiểm tra node được chọn
for idx in selected_nodes:
    selected_node = nodes[idx]
    st.header(f"Selected Node: {selected_node.message}")

    # Hiển thị toàn bộ ngữ cảnh hội thoại từ gốc đến node đã chọn
    st.subheader("Conversation Context")
    display_conversation(selected_node)

    # Cho phép người dùng nhập request để lấy kết quả mới và gán cho node
    request = st.text_input(f"Enter request for {selected_node.message}", key=f"request_{idx}")
    if st.button("Get Result", key=f"get_result_{idx}"):
        result = ketqua(request)
        selected_node.message = result  # Gán kết quả mới cho node
        st.write(f"Updated Node Message: {result}")

    # Hiển thị các node con của node đã chọn (nếu có)
    st.subheader("Child Nodes")
    if selected_node.children:
        for child in selected_node.children:
            st.write(f"- {child.message}")
    else:
        st.write("No child nodes available.")

    # Thêm node mới nếu là node cuối cùng
    if not selected_node.children:
        new_node_message = st.text_input("Enter message for new child node", key=f"new_node_{idx}")
        if st.button("Add New Node", key=f"add_node_{idx}"):
            new_node = Node(message=new_node_message, parent=selected_node)
            st.write(f"Added new node: {new_node_message}")
