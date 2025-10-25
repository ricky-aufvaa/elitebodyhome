# Elite Body Home - React Chatbot Frontend

A modern React.js chatbot interface for the Elite Body Home AI Assistant.

## Features

- **Full-screen responsive layout** with input at the bottom
- **React.js architecture** with component-based design
- **Real-time chat** with typing indicators
- **Markdown support** for rich bot responses using react-markdown
- **Error handling** with user-friendly messages
- **Auto-scroll** to latest messages
- **API integration** with axios
- **Modern styling** with CSS modules

## Project Structure

```
frontend/
├── public/
│   └── index.html          # HTML template
├── src/
│   ├── components/         # React components
│   │   ├── ChatContainer.js    # Main chat container
│   │   ├── ChatHeader.js       # Header component
│   │   ├── MessageList.js      # Message list container
│   │   ├── Message.js          # Individual message component
│   │   ├── ChatInput.js        # Input component
│   │   ├── TypingIndicator.js  # Typing animation
│   │   └── *.css              # Component styles
│   ├── services/
│   │   └── api.js             # API service layer
│   ├── App.js                 # Main App component
│   ├── App.css                # Global styles
│   ├── index.js               # React entry point
│   └── index.css              # Base styles
├── package.json               # Dependencies and scripts
└── README.md                  # This file
```

## Installation & Setup

1. **Install Dependencies**:
   ```bash
   cd frontend
   npm install
   ```

2. **Start the Backend API**:
   ```bash
   # From the root directory
   python app.py
   ```
   The API should be running on `http://localhost:8000`

3. **Start the React Development Server**:
   ```bash
   npm start
   ```
   The frontend will open at `http://localhost:3000`

## Available Scripts

- `npm start` - Runs the app in development mode
- `npm build` - Builds the app for production
- `npm test` - Launches the test runner
- `npm eject` - Ejects from Create React App (irreversible)

## Dependencies

### Core Dependencies
- **React 18.2.0** - UI library
- **React DOM 18.2.0** - DOM rendering
- **React Scripts 5.0.1** - Build tools and configuration
- **Axios 1.6.0** - HTTP client for API calls
- **React Markdown 9.0.1** - Markdown rendering for bot responses
- **Remark GFM 4.0.0** - GitHub Flavored Markdown support

### Dev Dependencies
- **@types/react** - TypeScript definitions
- **@types/react-dom** - TypeScript definitions

## API Integration

The frontend connects to the FastAPI backend at `http://localhost:8000/chat`. 

### API Configuration
Edit `src/services/api.js` to change the API URL:
```javascript
const API_BASE_URL = 'http://your-api-url:port';
```

### API Endpoints Used
- `POST /chat` - Send messages to the AI
- `GET /health` - Health check (for connection testing)

## Component Architecture

### ChatContainer
- Main container managing chat state
- Handles message sending and receiving
- Manages loading states and errors

### Message Components
- **MessageList**: Renders list of messages
- **Message**: Individual message with markdown support
- **TypingIndicator**: Animated typing dots

### Input Components
- **ChatInput**: Text input with send button
- **ChatHeader**: Title and description

## Styling

- **CSS Modules** approach with component-specific styles
- **Responsive design** for mobile and desktop
- **Modern gradients** and animations
- **Professional medical/wellness theme**

## Customization

### Changing Colors
Edit the CSS files to modify the color scheme:
- Primary gradient: `#667eea` to `#764ba2`
- Header gradient: `#2c3e50` to `#34495e`
- Background: `#f8f9fa`

### Adding Features
The modular React architecture makes it easy to add:
- Message history persistence
- File upload support
- Voice input/output
- Quick action buttons
- User authentication

## Debug Mode

Add `?debug=true` to the URL to see API metadata below bot messages:
```
http://localhost:3000?debug=true
```

## Browser Compatibility

- Modern browsers (Chrome, Firefox, Safari, Edge)
- Mobile browsers (iOS Safari, Chrome Mobile)
- Responsive design for all screen sizes

## Troubleshooting

### "Cannot connect to AI service" error
- Ensure the FastAPI backend is running on port 8000
- Check browser console for CORS errors
- Verify the API URL in `src/services/api.js`

### Build errors
- Delete `node_modules` and run `npm install`
- Clear npm cache: `npm cache clean --force`
- Check Node.js version compatibility

### Styling issues
- Check for CSS import errors
- Verify all CSS files are properly linked
- Clear browser cache

## Production Build

To create a production build:
```bash
npm run build
```

This creates a `build` folder with optimized files ready for deployment.

## Deployment

The built React app can be deployed to:
- **Netlify** - Drag and drop the build folder
- **Vercel** - Connect your Git repository
- **AWS S3** - Upload build files to S3 bucket
- **Any static hosting service**

Make sure to update the API URL for production deployment.
