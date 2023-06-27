%
% EEGLAB Required! 
% command: eeglab
% 
%%
seed_num = 9999;
fs = 500;
n = 80;
%%
labels = {'left', 'right'};
rng(seed_num);
label_patterns = labels(randi(numel(labels), 1, n));

%%
start_index = 500;
step = 500;
indexes = start_index + (0:step:(n-1)*step);

%%
rng(seed_num);
dummy_signal = rand(64, n*fs+fs);

%% eeglab
left_indexes = strcmp(label_patterns, labels{1});
right_indexes = strcmp(label_patterns, labels{2});
eeg = pop_importdata('dataformat', 'array', 'data', dummy_signal, 'setname', 'EEG', 'srate', fs);

eeg = eeg_addnewevents(eeg,{indexes(left_indexes) indexes(right_indexes)},{'left' 'right'});
eeg = pop_eegfiltnew(eeg,1,[]);
eeg = pop_eegfiltnew(eeg,[],30);
eeg = pop_epoch(eeg, labels, [0, 1]);
pop_saveset(eeg,"filename",convertStringsToChars("./test.set"));