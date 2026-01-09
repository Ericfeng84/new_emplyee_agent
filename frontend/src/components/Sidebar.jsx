import React from 'react';
import { Plus, MessageSquare, Settings, LogOut } from 'lucide-react';
import styles from './Sidebar.module.css';

const Sidebar = ({ onNewChat }) => {
    return (
        <aside className={styles.sidebar}>
            <div className={styles.header}>
                <div className={styles.logo}>
                    <div className={styles.logoIcon} />
                    <span>Nexus Agent</span>
                </div>
                <button className={styles.newChatBtn} onClick={onNewChat}>
                    <Plus size={20} />
                    <span>New Chat</span>
                </button>
            </div>

            <div className={styles.content}>
                <div className={styles.sectionTitle}>Recent Chats</div>
                <div className={styles.sessionList}>
                    {/* Mock Data */}
                    <div className={`${styles.sessionItem} ${styles.active}`}>
                        <MessageSquare size={18} />
                        <span className={styles.sessionTitle}>Welcome to Nexus</span>
                    </div>
                    <div className={styles.sessionItem}>
                        <MessageSquare size={18} />
                        <span className={styles.sessionTitle}>Employee Hando...</span>
                    </div>
                    <div className={styles.sessionItem}>
                        <MessageSquare size={18} />
                        <span className={styles.sessionTitle}>IT Support</span>
                    </div>
                </div>
            </div>

            <div className={styles.footer}>
                <button className={styles.footerBtn}>
                    <Settings size={20} />
                    <span>Settings</span>
                </button>
                {/* <button className={styles.footerBtn}>
          <LogOut size={20} />
        </button> */}
            </div>
        </aside>
    );
};

export default Sidebar;
