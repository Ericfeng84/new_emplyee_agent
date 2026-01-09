# Sprint 6: Frontend Development Documentation

## Overview

This document provides a comprehensive overview of the Nexus Agent frontend implementation, covering architecture, components, state management, API integration, and development guidelines.

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Project Structure](#project-structure)
3. [Core Components](#core-components)
4. [State Management](#state-management)
5. [API Integration](#api-integration)
6. [Styling Approach](#styling-approach)
7. [Key Features](#key-features)
8. [Development Guidelines](#development-guidelines)
9. [Testing Strategy](#testing-strategy)
10. [Future Improvements](#future-improvements)

---

## Architecture Overview

### Technology Stack

- **Framework**: React 18 with Hooks
- **Build Tool**: Vite
- **HTTP Client**: Axios
- **UI Icons**: Lucide React
- **Markdown Rendering**: React Markdown
- **Styling**: CSS Modules
- **Package Manager**: npm

### Design Patterns

- **Component-Based Architecture**: Modular, reusable components
- **Optimistic UI Updates**: Immediate feedback for user actions
- **Session Persistence**: LocalStorage for session management
- **Error Boundaries**: Graceful error handling
- **Separation of Concerns**: Clear separation between UI and business logic

### Application Flow

```
User Input → ChatWindow → App Component → API Client → Backend
                ↓
          State Update → UI Re-render
```

---

## Project Structure

```
frontend/
├── src/
│   ├── api/
│   │   └── client.js              # API client with axios
│   ├── components/
│   │   ├── ChatWindow.jsx         # Main chat interface
│   │   ├── ChatWindow.module.css  # Chat window styles
│   │   ├── Sidebar.jsx            # Navigation sidebar
│   │   └── Sidebar.module.css     # Sidebar styles
│   ├── App.jsx                    # Root application component
│   ├── App.css                    # Global styles
│   ├── main.jsx                   # Application entry point
│   └── index.css                  # Base CSS
├── public/                        # Static assets
├── index.html                     # HTML template
├── package.json                   # Dependencies
├── vite.config.js                 # Vite configuration
└── eslint.config.js               # ESLint configuration
```

---

## Core Components

### 1. App Component (`App.jsx`)

**Purpose**: Root component managing application state and orchestration.

**State Management**:
```javascript
const [messages, setMessages] = useState([]);        // Chat messages
const [sessionId, setSessionId] = useState(null);    // Current session ID
const [isLoading, setIsLoading] = useState(false);    // Loading state
```

**Key Functions**:

#### Session Initialization
```javascript
useEffect(() => {
  const initSession = async () => {
    // Check localStorage for existing session
    const storedSession = localStorage.getItem('nexus_session_id');
    if (storedSession) {
      setSessionId(storedSession);
      // Load conversation history
      const history = await api.getSessionHistory(storedSession);
      setMessages(formatHistory(history));
    } else {
      await createNewSession();
    }
  };
  initSession();
}, []);
```

**Features**:
- Automatic session restoration from localStorage
- Conversation history loading on app start
- Graceful fallback to new session if history fails

#### Message Handling
```javascript
const handleSendMessage = async (text) => {
  // Optimistic UI update
  const userMsg = { role: 'user', content: text };
  setMessages((prev) => [...prev, userMsg]);
  
  // API call
  const response = await api.sendMessage(sessionId, text);
  
  // Update with assistant response
  const assistantMsg = {
    role: 'assistant',
    content: response.choices[0].message.content
  };
  setMessages((prev) => [...prev, assistantMsg]);
};
```

**Best Practices**:
- Optimistic UI updates for immediate feedback
- Error handling with user-friendly messages
- Loading state management
- Session validation before API calls

---

### 2. ChatWindow Component (`ChatWindow.jsx`)

**Purpose**: Main chat interface displaying messages and handling user input.

**Props**:
```javascript
{
  messages: Array,      // Array of message objects
  onSendMessage: Function  // Callback for sending messages
}
```

**Key Features**:

#### Message Display
```javascript
{messages.map((msg, index) => (
  <div className={`${styles.message} ${msg.role === 'user' ? styles.userMessage : styles.agentMessage}`}>
    <div className={styles.messageContent}>
      {msg.role === 'assistant' ? (
        <ReactMarkdown>{msg.content}</ReactMarkdown>
      ) : (
        msg.content
      )}
    </div>
  </div>
))}
```

**Features**:
- Markdown rendering for assistant responses
- Different styling for user vs. agent messages
- Auto-scroll to latest message
- Empty state with helpful prompts

#### Input Handling
```javascript
const handleKeyPress = (e) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    handleSend();
  }
};
```

**Features**:
- Enter to send, Shift+Enter for new line
- Disabled send button when input is empty
- Visual feedback for active state

---

### 3. Sidebar Component (`Sidebar.jsx`)

**Purpose**: Navigation sidebar for chat history and settings.

**Props**:
```javascript
{
  onNewChat: Function  // Callback for creating new chat
}
```

**Key Features**:
- New chat button
- Recent chats list (currently mock data)
- Settings button
- Responsive design

**Future Enhancements**:
- Real chat history from API
- Session switching
- Chat deletion
- Search functionality

---

## State Management

### Local State vs. Global State

**Current Approach**: Local state with React Hooks

**Rationale**:
- Simple application with limited state
- No need for complex state management (Redux, Context API)
- Props drilling is minimal
- Performance is acceptable

### State Flow

```
App Component (State Owner)
    ↓ props
ChatWindow (Display)
    ↓ callback
onSendMessage → App → API Client
```

### State Persistence

**Session ID**: Stored in `localStorage`
```javascript
localStorage.setItem('nexus_session_id', data.session_id);
```

**Conversation History**: Loaded from API on session restore

---

## API Integration

### API Client (`client.js`)

**Configuration**:
```javascript
const client = axios.create({
  baseURL: 'http://localhost:8001/v1',
  headers: { 'Content-Type': 'application/json' },
  withCredentials: true,  // CORS credentials
  timeout: 30000,         // 30 second timeout
});
```

### API Methods

#### 1. Create Session
```javascript
api.createSession(userId = 'demo_user')
// Returns: { session_id: "..." }
```

**Usage**: Initialize new conversation session

#### 2. Get Session History
```javascript
api.getSessionHistory(sessionId)
// Returns: Array of message objects
```

**Usage**: Load conversation history for existing session

#### 3. Send Message
```javascript
api.sendMessage(sessionId, message, userId = 'demo_user')
// Returns: { choices: [{ message: { content: "..." } }] }
```

**Usage**: Send user message and get agent response

#### 4. Health Check
```javascript
api.healthCheck()
// Returns: Health status object
```

**Usage**: Verify backend availability

### Error Handling

**Request Interceptor**:
```javascript
client.interceptors.request.use(
  (config) => {
    console.log(`[API] ${config.method.toUpperCase()} ${config.url}`, config.data);
    return config;
  },
  (error) => {
    console.error('[API] Request error:', error);
    return Promise.reject(error);
  }
);
```

**Response Interceptor**:
```javascript
client.interceptors.response.use(
  (response) => {
    console.log(`[API] Response ${response.status}:`, response.data);
    return response;
  },
  (error) => {
    // Detailed error logging
    // Status code handling (401, 403, 404, 405, 500+)
    // Network error detection
    return Promise.reject(error);
  }
);
```

**Error Cases Handled**:
- 401: Unauthorized
- 403: Forbidden
- 404: Not found
- 405: Method not allowed (CORS)
- 500+: Server errors
- Network errors
- Configuration errors

---

## Styling Approach

### CSS Modules

**Why CSS Modules**:
- Scoped styles prevent conflicts
- Better maintainability
- Clear component-style relationship
- No need for BEM naming convention

**Example**:
```javascript
import styles from './ChatWindow.module.css';

<div className={styles.chatWindow}>
  <div className={styles.header}>
    <h2 className={styles.title}>Nexus Assistant</h2>
  </div>
</div>
```

### Design System

**Color Palette**:
- Primary: Blue/indigo tones
- Background: Light gray/white
- Text: Dark gray
- Accent: Green for success, red for errors

**Typography**:
- Clean, readable fonts
- Consistent sizing hierarchy
- Good line height for readability

**Spacing**:
- Consistent padding/margins
- Responsive gaps
- Visual hierarchy through spacing

---

## Key Features

### 1. Session Management

**Features**:
- Automatic session creation
- Session persistence across page reloads
- Conversation history restoration
- Multiple session support (backend ready)

**Implementation**:
```javascript
// Session ID storage
localStorage.setItem('nexus_session_id', sessionId);

// Session restoration
const storedSession = localStorage.getItem('nexus_session_id');
if (storedSession) {
  await loadHistory(storedSession);
}
```

### 2. Optimistic UI Updates

**Benefits**:
- Instant feedback to user
- Improved perceived performance
- Better user experience

**Implementation**:
```javascript
// Add user message immediately
setMessages((prev) => [...prev, userMsg]);

// Then fetch response
const response = await api.sendMessage(sessionId, text);

// Add assistant response
setMessages((prev) => [...prev, assistantMsg]);
```

### 3. Markdown Rendering

**Features**:
- Rich text formatting for assistant responses
- Code syntax highlighting (future)
- Lists, links, headers support

**Implementation**:
```javascript
<ReactMarkdown>{msg.content}</ReactMarkdown>
```

### 4. Auto-Scroll

**Features**:
- Automatically scroll to latest message
- Smooth scrolling animation
- Works with new messages

**Implementation**:
```javascript
const messagesEndRef = useRef(null);

const scrollToBottom = () => {
  messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
};

useEffect(() => {
  scrollToBottom();
}, [messages]);
```

### 5. Error Handling

**Features**:
- User-friendly error messages
- Console logging for debugging
- Graceful degradation
- Network error detection

**Implementation**:
```javascript
try {
  const response = await api.sendMessage(sessionId, text);
  setMessages((prev) => [...prev, assistantMsg]);
} catch (err) {
  console.error("Chat error:", err);
  setMessages((prev) => [...prev, {
    role: 'system',
    content: "Error: Failed to get response from agent. Please try again."
  }]);
}
```

---

## Development Guidelines

### Code Style

**Component Structure**:
```javascript
// 1. Imports
import React, { useState, useEffect } from 'react';
import Component from './Component';

// 2. Component definition
const MyComponent = ({ prop1, prop2 }) => {
  // 3. State
  const [state, setState] = useState(initialValue);
  
  // 4. Refs
  const ref = useRef(null);
  
  // 5. Effects
  useEffect(() => {
    // Effect logic
  }, [dependencies]);
  
  // 6. Handlers
  const handleEvent = () => {
    // Handler logic
  };
  
  // 7. Render
  return (
    <div>
      {/* JSX */}
    </div>
  );
};

// 8. Export
export default MyComponent;
```

### Naming Conventions

- **Components**: PascalCase (`ChatWindow`, `Sidebar`)
- **Functions**: camelCase (`handleSendMessage`, `createNewSession`)
- **Constants**: UPPER_SNAKE_CASE (`API_BASE_URL`)
- **CSS Classes**: camelCase from CSS Modules (`styles.chatWindow`)

### Best Practices

1. **Component Composition**:
   - Keep components small and focused
   - Extract reusable logic into custom hooks
   - Use props for data flow

2. **Performance**:
   - Use `useCallback` for event handlers
   - Use `useMemo` for expensive computations
   - Avoid unnecessary re-renders

3. **Accessibility**:
   - Use semantic HTML
   - Add ARIA labels where needed
   - Ensure keyboard navigation works

4. **Error Handling**:
   - Always handle API errors
   - Provide user-friendly error messages
   - Log errors for debugging

5. **Code Organization**:
   - Group related code together
   - Add clear comments
   - Follow consistent formatting

### Git Workflow

**Commit Message Format**:
```
type(scope): description

Examples:
feat(chat): add message input validation
fix(api): handle network errors gracefully
style(sidebar): improve responsive design
docs(readme): update installation instructions
```

**Branch Naming**:
- `feature/feature-name`
- `fix/bug-description`
- `refactor/component-name`

---

## Testing Strategy

### Unit Testing

**Tools**: Jest + React Testing Library

**Test Coverage**:
- Component rendering
- User interactions
- State changes
- API calls (mocked)

**Example Test**:
```javascript
import { render, screen, fireEvent } from '@testing-library/react';
import ChatWindow from './ChatWindow';

test('sends message when send button is clicked', () => {
  const mockOnSend = jest.fn();
  render(<ChatWindow messages={[]} onSendMessage={mockOnSend} />);
  
  const input = screen.getByPlaceholderText('Type your message...');
  fireEvent.change(input, { target: { value: 'Hello' } });
  
  const sendBtn = screen.getByRole('button', { name: /send/i });
  fireEvent.click(sendBtn);
  
  expect(mockOnSend).toHaveBeenCalledWith('Hello');
});
```

### Integration Testing

**Tools**: Cypress or Playwright

**Test Scenarios**:
- End-to-end user flows
- API integration
- Session management
- Error handling

### Manual Testing Checklist

- [ ] Session creation and restoration
- [ ] Message sending and receiving
- [ ] Markdown rendering
- [ ] Auto-scroll functionality
- [ ] Error handling
- [ ] Responsive design
- [ ] Keyboard navigation
- [ ] Loading states

---

## Future Improvements

### Short-term (Sprint 7)

1. **Real Chat History**
   - Implement session list API
   - Display actual chat history in sidebar
   - Add session switching

2. **Enhanced Error Handling**
   - Retry mechanism for failed requests
   - Offline detection
   - Better error messages

3. **Loading States**
   - Typing indicator
   - Skeleton screens
   - Progress indicators

### Medium-term (Sprint 8-9)

1. **Rich Media Support**
   - Image upload
   - File attachments
   - Voice input

2. **Advanced Features**
   - Message search
   - Chat export
   - Message editing
   - Message deletion

3. **UI Enhancements**
   - Dark mode
   - Custom themes
   - Font size adjustment
   - Accessibility improvements

### Long-term (Sprint 10+)

1. **Performance Optimization**
   - Virtual scrolling for long conversations
   - Message pagination
   - Caching strategies

2. **Advanced Interactions**
   - Streaming responses
   - Real-time updates (WebSocket)
   - Multi-user support

3. **Analytics**
   - Usage tracking
   - Error monitoring
   - Performance metrics

---

## Deployment

### Build Process

```bash
# Install dependencies
npm install

# Development server
npm run dev

# Production build
npm run build

# Preview production build
npm run preview
```

### Environment Variables

Create `.env` file:
```
VITE_API_BASE_URL=http://localhost:8001/v1
VITE_APP_TITLE=Nexus Agent
```

### Deployment Options

1. **Static Hosting**: Netlify, Vercel, GitHub Pages
2. **Docker**: Containerized deployment
3. **CDN**: CloudFront, Cloudflare

---

## Troubleshooting

### Common Issues

**1. CORS Errors**
- Check backend CORS configuration
- Verify `withCredentials: true` in axios config
- Ensure backend is running on correct port

**2. Session Not Persisting**
- Check localStorage is enabled
- Verify session ID is being saved
- Check for localStorage quota exceeded

**3. Messages Not Displaying**
- Verify message format matches expected structure
- Check CSS module imports
- Ensure messages array is being updated

**4. API Calls Failing**
- Check backend is running
- Verify API base URL
- Check network tab in browser dev tools
- Review console for error messages

### Debugging Tips

1. **Enable React DevTools**
2. **Use console.log strategically**
3. **Check Network tab for API calls**
4. **Monitor Redux DevTools (if added)**
5. **Use React Profiler for performance**

---

## References

### Documentation
- [React Documentation](https://react.dev)
- [Vite Documentation](https://vitejs.dev)
- [Axios Documentation](https://axios-http.com)
- [Lucide React Icons](https://lucide.dev)
- [React Markdown](https://github.com/remarkjs/react-markdown)

### Best Practices
- [React Best Practices](https://react.dev/learn/thinking-in-react)
- [CSS Modules](https://github.com/css-modules/css-modules)
- [TypeScript with React](https://react-typescript-cheatsheet.netlify.app/)

---

## Conclusion

This frontend implementation provides a solid foundation for the Nexus Agent chat interface. The architecture is modular, maintainable, and follows React best practices. Future sprints will focus on enhancing features, improving performance, and adding advanced functionality.

**Key Strengths**:
- Clean, modular component architecture
- Robust error handling
- Optimistic UI updates
- Session persistence
- Comprehensive API integration

**Next Steps**:
- Implement real chat history
- Add comprehensive testing
- Enhance error handling
- Improve performance
- Add advanced features

---

**Document Version**: 1.0  
**Last Updated**: 2026-01-09  
**Author**: Nexus Agent Team  
**Status**: Complete
