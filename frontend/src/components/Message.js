import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import './Message.css';

const Message = ({ message }) => {
  const { type, content, metadata, timestamp } = message;

  const formatTime = (date) => {
    return new Date(date).toLocaleTimeString([], { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };

  return (
    <div className={`message ${type}-message`}>
      <div className="message-content">
        {type === 'bot' ? (
          <ReactMarkdown 
            remarkPlugins={[remarkGfm]}
            components={{
              // Custom components for better styling
              h1: ({children}) => <h1 className="message-h1">{children}</h1>,
              h2: ({children}) => <h2 className="message-h2">{children}</h2>,
              h3: ({children}) => <h3 className="message-h3">{children}</h3>,
              p: ({children}) => <p className="message-p">{children}</p>,
              ul: ({children}) => <ul className="message-ul">{children}</ul>,
              ol: ({children}) => <ol className="message-ol">{children}</ol>,
              li: ({children}) => <li className="message-li">{children}</li>,
              strong: ({children}) => <strong className="message-strong">{children}</strong>,
              code: ({children}) => <code className="message-code">{children}</code>,
              pre: ({children}) => <pre className="message-pre">{children}</pre>,
            }}
          >
            {content}
          </ReactMarkdown>
        ) : (
          <p>{content}</p>
        )}
        
        {/* Debug metadata (only show if URL has debug=true) */}
        {metadata && window.location.search.includes('debug=true') && (
          <div className="message-metadata">
            <small>
              On-topic: {metadata.on_topic ? 'Yes' : 'No'} | 
              Documents: {metadata.documents_retrieved} | 
              Time: {metadata.processing_time}s
            </small>
          </div>
        )}
      </div>
      
      <div className="message-time">
        {formatTime(timestamp)}
      </div>
    </div>
  );
};

export default Message;
