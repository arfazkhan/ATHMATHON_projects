import React from "react";
import styles from "@chatscope/chat-ui-kit-styles/dist/default/styles.min.css";
import {
  MainContainer,
  ChatContainer,
  MessageList,
  Message,
  MessageInput,
} from "@chatscope/chat-ui-kit-react";
const Chat = () => {
  return (
    <div className="relative px-5" style={{ height: "calc(100vh - 200px )" }}>
      <h1 className="mt-4 text-center mb-2 font-bold text-xl">
        Community chat
      </h1>
      <MainContainer>
        <ChatContainer>
          <MessageList>
            <Message
              model={{
                message: "Hello my friend",
                sentTime: "just now",
                sender: "Joe",
              }}
            />
            <Message
              model={{
                message: "Hello my friend",
                sentTime: "just now",
              }}
            />
          </MessageList>
          <MessageInput placeholder="Type message here" />
        </ChatContainer>
      </MainContainer>
    </div>
  );
};

export default Chat;
