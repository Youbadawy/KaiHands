
import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { FaShareAlt } from 'react-icons/fa';
import { Container } from '#/components/layout/container';
import { useConversationId } from '#/hooks/use-conversation-id';

export function SocialMediaTab() {
  const { t } = useTranslation();
  const { conversationId } = useConversationId();
  
  const [selectedPlatform, setSelectedPlatform] = useState<string>('');
  
  const platforms = [
    { id: 'twitter', name: 'Twitter/X', icon: 'twitter' },
    { id: 'reddit', name: 'Reddit', icon: 'reddit' },
    { id: 'linkedin', name: 'LinkedIn', icon: 'linkedin' },
    { id: 'facebook', name: 'Facebook', icon: 'facebook' },
    { id: 'instagram', name: 'Instagram', icon: 'instagram' },
    { id: 'tiktok', name: 'TikTok', icon: 'tiktok' },
  ];
  
  return (
    <Container
      className="h-full w-full"
      labels={[
        {
          label: "Social Media",
          to: "",
          icon: <FaShareAlt className="w-6 h-6" />,
        },
      ]}
    >
      <div className="h-full w-full p-6">
        <div className="flex flex-col gap-6">
          <h2 className="text-xl font-bold">Social Media Management</h2>
          
          <div className="grid grid-cols-2 gap-4">
            {platforms.map((platform) => (
              <div key={platform.id} className="border rounded-lg p-4">
                <h3 className="font-semibold mb-2">{platform.name}</h3>
                <button 
                  className="bg-blue-500 text-white px-4 py-2 rounded"
                  onClick={() => setSelectedPlatform(platform.id)}
                >
                  Connect {platform.name}
                </button>
              </div>
            ))}
          </div>
          
          {selectedPlatform && (
            <div className="border rounded-lg p-4">
              <h3>Connected to {selectedPlatform}</h3>
              <p>Social media management features coming soon...</p>
            </div>
          )}
        </div>
      </div>
    </Container>
  );
}
